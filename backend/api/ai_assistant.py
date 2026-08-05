import os
import json
from django.db.models import Count, Q
from .models import (
    Teacher,
    SchoolClass,
    Course,
    Classroom,
    TimeSlot,
    CourseRequirement,
    Schedule
)

# Tool execution functions for Gemini AI
def get_schedule_summary():
    """Returns general summary statistics about the school schedule, teachers, classes, and classrooms."""
    total_teachers = Teacher.objects.count()
    total_classes = SchoolClass.objects.count()
    total_classrooms = Classroom.objects.count()
    total_courses = Course.objects.count()
    total_requirements = CourseRequirement.objects.count()
    total_assigned_hours = Schedule.objects.count()
    
    # Check classes with complete or incomplete schedules
    classes = SchoolClass.objects.all()
    class_stats = []
    for sc in classes:
        required_hours = sum(cr.weekly_hours for cr in CourseRequirement.objects.filter(school_class=sc))
        assigned_hours = Schedule.objects.filter(school_class=sc).count()
        class_stats.append({
            "class_name": sc.name,
            "required_hours": required_hours,
            "assigned_hours": assigned_hours,
            "status": "Tamamlandı" if assigned_hours >= required_hours and required_hours > 0 else "Eksik/Atanmamış"
        })

    return {
        "total_teachers": total_teachers,
        "total_classes": total_classes,
        "total_classrooms": total_classrooms,
        "total_courses": total_courses,
        "total_requirements": total_requirements,
        "total_assigned_hours": total_assigned_hours,
        "class_details": class_stats
    }


def get_teacher_schedule(teacher_name: str):
    """Retrieves weekly schedule and off-day for a specific teacher by name."""
    teachers = Teacher.objects.filter(name__icontains=teacher_name)
    if not teachers.exists():
        return {"error": f"'{teacher_name}' adında bir öğretmen bulunamadı."}
    
    teacher = teachers.first()
    schedules = Schedule.objects.filter(teacher=teacher).select_related('school_class', 'course', 'classroom', 'time_slot')
    
    assigned_lessons = []
    for s in schedules:
        assigned_lessons.append({
            "day": s.time_slot.day,
            "hour": s.time_slot.hour,
            "clock_time": s.time_slot.time_range_str,
            "class": s.school_class.name,
            "course": s.course.name,
            "classroom": s.classroom.name
        })
    
    return {
        "teacher_name": teacher.name,
        "branch": teacher.branch,
        "off_day": teacher.off_day,
        "total_assigned_hours": len(assigned_lessons),
        "schedule": assigned_lessons
    }


def get_class_schedule(class_name: str):
    """Retrieves weekly schedule for a specific school class (e.g. 10-A, 9-B)."""
    classes = SchoolClass.objects.filter(name__icontains=class_name)
    if not classes.exists():
        return {"error": f"'{class_name}' adında bir sınıf bulunamadı."}
    
    school_class = classes.first()
    schedules = Schedule.objects.filter(school_class=school_class).select_related('course', 'teacher', 'classroom', 'time_slot')
    
    assigned_lessons = []
    for s in schedules:
        assigned_lessons.append({
            "day": s.time_slot.day,
            "hour": s.time_slot.hour,
            "clock_time": s.time_slot.time_range_str,
            "course": s.course.name,
            "teacher": s.teacher.name,
            "classroom": s.classroom.name
        })
        
    return {
        "class_name": school_class.name,
        "grade_level": school_class.grade_level,
        "total_assigned_hours": len(assigned_lessons),
        "schedule": assigned_lessons
    }


def check_teacher_availability(teacher_name: str, day: str, hour: int):
    """Checks if a teacher is available at a given day and hour slot."""
    teachers = Teacher.objects.filter(name__icontains=teacher_name)
    if not teachers.exists():
        return {"error": f"'{teacher_name}' adında öğretmen bulunamadı."}
    
    teacher = teachers.first()
    if teacher.off_day and teacher.off_day.lower() == day.lower():
        return {
            "available": False,
            "reason": f"{teacher.name} öğretmenin izin günü ({teacher.off_day})."
        }
    
    schedule_exists = Schedule.objects.filter(
        teacher=teacher,
        time_slot__day__iexact=day,
        time_slot__hour=hour
    ).select_related('school_class', 'course', 'time_slot').first()
    
    if schedule_exists:
        return {
            "available": False,
            "reason": f"{teacher.name} öğretmenin {day} {hour}. saatte ({schedule_exists.time_slot.time_range_str}) {schedule_exists.school_class.name} sınıfına {schedule_exists.course.name} dersi var."
        }
    
    return {
        "available": True,
        "reason": f"{teacher.name} öğretmen {day} {hour}. saatte müsait."
    }


def get_empty_classrooms(day: str, hour: int, is_lab: bool = False):
    """Returns classrooms that are empty at a specific day and hour slot."""
    occupied_classroom_ids = Schedule.objects.filter(
        time_slot__day__iexact=day,
        time_slot__hour=hour
    ).values_list('classroom_id', flat=True)
    
    available_classrooms = Classroom.objects.exclude(id__in=occupied_classroom_ids)
    if is_lab:
        available_classrooms = available_classrooms.filter(is_lab=True)
        
    result = []
    for c in available_classrooms:
        result.append({
            "id": c.id,
            "name": c.name,
            "capacity": c.capacity,
            "is_lab": c.is_lab
        })
    return {
        "day": day,
        "hour": hour,
        "is_lab_filter": is_lab,
        "count": len(result),
        "available_classrooms": result
    }


def explain_schedule_conflicts():
    """Analyzes overall bottlenecks in requirements vs available teachers, time slots, and classrooms."""
    requirements = CourseRequirement.objects.select_related('teacher', 'course', 'school_class').all()
    time_slots_count = TimeSlot.objects.count()
    classrooms = Classroom.objects.all()
    lab_classrooms_count = classrooms.filter(is_lab=True).count()

    issues = []

    # Check teacher workload vs available slots
    teachers = Teacher.objects.all()
    for t in teachers:
        t_reqs = CourseRequirement.objects.filter(teacher=t)
        total_hours = sum(r.weekly_hours for r in t_reqs)
        available_slots = time_slots_count
        if t.off_day:
            days_count = TimeSlot.objects.values('day').distinct().count()
            if days_count > 0:
                slots_per_day = time_slots_count / days_count
                available_slots -= slots_per_day

        if total_hours > available_slots:
            issues.append(f"Öğretmen Yük Aşımı: {t.name} öğretmeninin {total_hours} saat dersi var ama sadece {int(available_slots)} müsait saati var.")

    # Check lab requirement vs lab capacity
    lab_required_hours = sum(r.weekly_hours for r in requirements if r.course.is_lab_required)
    if lab_classrooms_count == 0 and lab_required_hours > 0:
        issues.append(f"Laboratuvar Eksikliği: Toplam {lab_required_hours} saat lab gerektiren ders var fakat sistemde hiç Laboratuvar dersliği yok!")
    elif lab_classrooms_count > 0:
        max_possible_lab_hours = lab_classrooms_count * time_slots_count
        if lab_required_hours > max_possible_lab_hours:
            issues.append(f"Laboratuvar Kapasite Yetersizliği: İstenen {lab_required_hours} lab saati, mevcut lab kapasitesini ({max_possible_lab_hours}) aşıyor.")

    # Check class requirement vs available slots
    classes = SchoolClass.objects.all()
    for sc in classes:
        c_reqs = CourseRequirement.objects.filter(school_class=sc)
        total_hours = sum(r.weekly_hours for r in c_reqs)
        if total_hours > time_slots_count:
            issues.append(f"Sınıf Ders Saati Aşımı: {sc.name} sınıfının toplam {total_hours} saat ders gereksinimi var ancak sistemde yalnızca {time_slots_count} zaman dilimi tanımlı.")

    if not issues:
        return {
            "status": "Çakışma veya aşırı yükleme tespit edilmedi.",
            "issues": ["Tüm öğretmen ders saatleri ve derslik kapasiteleri mevcut zaman dilimleriyle uyumlu görünüyor."]
        }
    
    return {
        "status": "Olası Çakışmalar / Darboğazlar Bulundu",
        "issues": issues
    }

# Mapping functions for Gemini tool calls
TOOL_FUNCTIONS = {
    "get_schedule_summary": get_schedule_summary,
    "get_teacher_schedule": get_teacher_schedule,
    "get_class_schedule": get_class_schedule,
    "check_teacher_availability": check_teacher_availability,
    "get_empty_classrooms": get_empty_classrooms,
    "explain_schedule_conflicts": explain_schedule_conflicts,
}


SYSTEM_PROMPT = """Sen 'Ders Programı Optimizasyon ve Yönetim Sistemi' için özel olarak tasarlanmış nazik, akıllı ve uzman bir Yapay Zeka Asistanısın (AI Assistant).

Görevin:
1. Okul idarecilerinin, öğretmenlerin ve kullanıcıların ders programı, derslikler, öğretmen müsaitlikleri ve sınıf dersleri hakkındaki sorularını yanıtlamak.
2. Sana sağlanan araçları (tools) kullanarak veritabanından güncel verileri çekmek ve kullanıcıya net, anlaşılır ve güzel biçimlendirilmiş Türkçe cevaplar vermek.
3. Sorulara yanıt verirken tablo, madde işaretleri (bullet points) ve vurgulu yazılar (bold) kullanarak okumayı kolaylaştırmak.
4. Eğer kullanıcı bir çakışma veya neden ders atanamadığı soruyorsa 'explain_schedule_conflicts' veya ilgili öğretmen/sınıf sorgu araçlarını kullanarak detaylı açıklama yapmak.
5. Her zaman Türkçe, yardımsever, profesyonel ve kurumsal bir dille yanıt ver.
"""


from dotenv import load_dotenv

def process_ai_chat(user_message: str, history: list = None) -> str:
    """Processes a user message using Google Gemini API with Tool Calling support."""
    load_dotenv(override=True)
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    
    if not api_key:
        return (
            "⚠️ **Gemini API Anahtarı Bulunamadı!**\n\n"
            "AI Asistanı kullanabilmek için lütfen `.env` dosyanıza geçerli bir `GEMINI_API_KEY` ekleyin.\n"
            "Ücretsiz API anahtarınızı [Google AI Studio](https://aistudio.google.com/) adresinden saniyeler içinde alabilirsiniz."
        )

    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        tools = list(TOOL_FUNCTIONS.values())

        contents = []
        if history:
            for item in history:
                role = "user" if item.get("role") == "user" else "model"
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=item.get("text", ""))]
                ))
        
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)]
        ))

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=tools,
            temperature=0.3
        )

        models_to_try = ['gemini-flash-latest', 'gemini-2.0-flash']
        response = None
        last_exception = None

        import time
        for model_name in models_to_try:
            for attempt in range(2):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=contents,
                        config=config
                    )
                    if response:
                        break
                except Exception as err:
                    last_exception = err
                    time.sleep(0.5)
            if response:
                break

        if response is None and last_exception:
            raise last_exception

        while response.function_calls:
            tool_response_parts = []
            for function_call in response.function_calls:
                fn_name = function_call.name
                fn_args = function_call.args or {}
                
                if fn_name in TOOL_FUNCTIONS:
                    try:
                        tool_result = TOOL_FUNCTIONS[fn_name](**fn_args)
                    except Exception as err:
                        tool_result = {"error": f"Fonksiyon çalıştırma hatası: {str(err)}"}
                else:
                    tool_result = {"error": f"Tanımsız araç: {fn_name}"}
                
                tool_response_parts.append(
                    types.Part.from_function_response(
                        name=fn_name,
                        response={"result": tool_result}
                    )
                )

            contents.append(response.candidates[0].content)
            contents.append(types.Content(role="user", parts=tool_response_parts))

            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )

        if response and response.text:
            return response.text
        return "Yanıt alınamadı. Lütfen sorunuzu tekrar iletin."

    except ImportError:
        return "⚠️ `google-genai` kütüphanesi backend ortamında kurulu değil. Lütfen `pip install google-genai` komutunu çalıştırın."
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            if "limit: 0" in error_msg.lower() or "limit 0" in error_msg.lower():
                return (
                    "⌛ **Google Gemini Model Kotası Yetersiz (Limit: 0)**\n\n"
                    "Google AI Studio hesabınızda bu model grubu için ücretsiz kullanım kotası 0 olarak tanımlanmış görünüyor.\n\n"
                    "👉 **Çözüm:**\n"
                    "1. [Google AI Studio](https://aistudio.google.com/) üzerinde yeni bir proje ile API Key oluşturmayı deneyin.\n"
                    "2. Veya Google Cloud konsolunda ücretsiz bir faturalandırma hesabı (Billing) ilişkilendirin."
                )
            return (
                "⌛ **Google Gemini Kota Limiti (Rate Limit)**\n\n"
                "API Anahtarınız doğrulandı! Ancak Google Gemini servisinin ücretsiz kullanım isteği limitine (dakikalık/günlük kota) ulaşıldı.\n\n"
                "👉 Lütfen **1-2 dakika bekleyip** tekrar bir mesaj gönderin."
            )
        if "API_KEY_INVALID" in error_msg or "API key not valid" in error_msg or "invalid api key" in error_msg.lower():
            return (
                "⚠️ **Geçersiz veya Eksik API Anahtarı!**\n\n"
                "Google Gemini API kullanabilmek için geçerli bir `GEMINI_API_KEY` gereklidir.\n\n"
                "📌 **Çözüm Adımları (Ücretsiz):**\n"
                "1. **[Google AI Studio](https://aistudio.google.com/)** adresine gidin.\n"
                "2. Ücretsiz API Anahtarı (**Get API Key**) oluşturup kopyalayın.\n"
                "3. Projenizdeki `.env` dosyasını açıp `GEMINI_API_KEY=kopyalanan_anahtar` şeklinde kaydedin."
            )
        return f"⚠️ **Yapay Zeka Asistan Hatası**: {error_msg}"
