from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Teacher,
    SchoolClass,
    Course,
    Classroom,
    TimeSlot,
    CourseRequirement,
    Schedule
)
from .serializers import (
    TeacherSerializer,
    SchoolClassSerializer,
    CourseSerializer,
    ClassroomSerializer,
    TimeSlotSerializer,
    CourseRequirementSerializer,
    ScheduleSerializer
)
from .scheduler import generate_schedule
from .ai_assistant import process_ai_chat

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

from datetime import datetime, time, timedelta
from rest_framework.decorators import action

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer

    @action(detail=False, methods=['post'], url_path='generate-default')
    def generate_default(self, request):
        start_time_raw = request.data.get('start_time', '08:30')
        lesson_duration = int(request.data.get('lesson_duration', 40))
        break_duration = int(request.data.get('break_duration', 10))
        lunch_after_hour = int(request.data.get('lunch_after_hour', 4))
        lunch_duration = int(request.data.get('lunch_duration', 50))
        hours_per_day = int(request.data.get('hours_per_day', 8))
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        try:
            base_start = datetime.strptime(start_time_raw, '%H:%M').time()
        except ValueError:
            base_start = time(8, 30)

        with transaction.atomic():
            # Delete existing schedules first if time slots change
            Schedule.objects.all().delete()
            TimeSlot.objects.all().delete()
            
            created_slots = []
            for day in days:
                current_time = datetime.combine(datetime.today(), base_start)
                for h in range(1, hours_per_day + 1):
                    slot_start = current_time.time()
                    current_time += timedelta(minutes=lesson_duration)
                    slot_end = current_time.time()
                    
                    slot = TimeSlot.objects.create(
                        day=day,
                        hour=h,
                        start_time=slot_start,
                        end_time=slot_end
                    )
                    created_slots.append(slot)

                    # Add break or lunch break
                    if h == lunch_after_hour:
                        current_time += timedelta(minutes=lunch_duration)
                    else:
                        current_time += timedelta(minutes=break_duration)

        serializer = self.get_serializer(created_slots, many=True)
        return Response({
            "message": f"Successfully generated {len(created_slots)} time slots with clock times.",
            "time_slots": serializer.data
        }, status=status.HTTP_201_CREATED)

class CourseRequirementViewSet(viewsets.ModelViewSet):
    queryset = CourseRequirement.objects.all()
    serializer_class = CourseRequirementSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.select_related('school_class', 'course', 'teacher', 'classroom', 'time_slot').all()
    serializer_class = ScheduleSerializer

    @action(detail=False, methods=['post'], url_path='move-lesson')
    def move_lesson(self, request):
        schedule_id = request.data.get('schedule_id')
        target_day = request.data.get('target_day')
        target_hour = request.data.get('target_hour')

        if not schedule_id or not target_day or target_hour is None:
            return Response({'error': 'schedule_id, target_day, and target_hour are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_hour = int(target_hour)
            schedule_item = Schedule.objects.select_related('teacher', 'school_class', 'classroom', 'time_slot').get(id=schedule_id)
            target_slot = TimeSlot.objects.filter(day__iexact=target_day, hour=target_hour).first()

            if not target_slot:
                return Response({'error': f'{target_day} günü {target_hour}. saat için tanımlı zaman dilimi bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)

            if schedule_item.time_slot_id == target_slot.id:
                return Response({'message': 'Ders zaten bu zaman diliminde.'}, status=status.HTTP_200_OK)

            teacher = schedule_item.teacher
            school_class = schedule_item.school_class
            classroom = schedule_item.classroom

            # 1. Check teacher off-day
            if teacher.off_day and teacher.off_day.lower() == target_day.lower():
                return Response({'error': f'{teacher.name} öğretmenin izin günü ({teacher.off_day}) olduğu için buraya ders taşınamaz!'}, status=status.HTTP_400_BAD_REQUEST)

            # 2. Check if teacher is busy elsewhere at target slot
            teacher_conflict = Schedule.objects.filter(
                teacher=teacher,
                time_slot=target_slot
            ).exclude(id=schedule_item.id).select_related('school_class').first()

            if teacher_conflict:
                return Response({'error': f'{teacher.name} öğretmenin {target_day} {target_hour}. saatte {teacher_conflict.school_class.name} sınıfına dersi var!'}, status=status.HTTP_400_BAD_REQUEST)

            # 3. Check if classroom is occupied by another class at target slot
            classroom_conflict = Schedule.objects.filter(
                classroom=classroom,
                time_slot=target_slot
            ).exclude(id=schedule_item.id).select_related('school_class').first()

            if classroom_conflict:
                return Response({'error': f'{classroom.name} dersliği {target_day} {target_hour}. saatte {classroom_conflict.school_class.name} sınıfı tarafından kullanılıyor!'}, status=status.HTTP_400_BAD_REQUEST)

            # 4. Check daily course limit for class on target day (max 3 hours per course per day)
            same_day_course_hours = Schedule.objects.filter(
                school_class=school_class,
                course=schedule_item.course,
                time_slot__day__iexact=target_day
            ).exclude(id=schedule_item.id).count()

            if same_day_course_hours >= 4:
                return Response({
                    'error': f'{school_class.name} sınıfının {target_day} gününde {schedule_item.course.name} dersi zaten {same_day_course_hours} saat tanımlı. Günde en fazla 4 saat aynı ders olabilir!'
                }, status=status.HTTP_400_BAD_REQUEST)


            # 5. Check teacher max daily hours limit on target day
            if teacher.max_daily_hours:
                teacher_day_hours = Schedule.objects.filter(
                    teacher=teacher,
                    time_slot__day__iexact=target_day
                ).exclude(id=schedule_item.id).count()

                if teacher_day_hours + 1 > teacher.max_daily_hours:
                    return Response({
                        'error': f'{teacher.name} öğretmenin {target_day} günündeki toplam ders sayısı ({teacher_day_hours + 1}), maksimum günlük ders sınırını ({teacher.max_daily_hours} saat) aşıyor!'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # 6. Check if target slot has another lesson for the SAME school_class (Swap case)
            class_existing_lesson = Schedule.objects.filter(
                school_class=school_class,
                time_slot=target_slot
            ).exclude(id=schedule_item.id).first()

            with transaction.atomic():
                if class_existing_lesson:
                    # Perform Swap between schedule_item and class_existing_lesson
                    old_slot = schedule_item.time_slot

                    # Check if class_existing_lesson's teacher can move to old_slot
                    existing_teacher = class_existing_lesson.teacher
                    if existing_teacher.off_day and existing_teacher.off_day.lower() == old_slot.day.lower():
                        return Response({'error': f'Takas yapılamaz! {existing_teacher.name} öğretmenin {old_slot.day} günü izin günü.'}, status=status.HTTP_400_BAD_REQUEST)

                    existing_teacher_conflict = Schedule.objects.filter(
                        teacher=existing_teacher,
                        time_slot=old_slot
                    ).exclude(id__in=[schedule_item.id, class_existing_lesson.id]).first()

                    if existing_teacher_conflict:
                        return Response({'error': f'Takas yapılamaz! {existing_teacher.name} öğretmenin {old_slot.day} {old_slot.hour}. saatte başka dersi var.'}, status=status.HTTP_400_BAD_REQUEST)

                    # Swap slots
                    schedule_item.time_slot = target_slot
                    class_existing_lesson.time_slot = old_slot
                    schedule_item.save()
                    class_existing_lesson.save()
                    msg = f"Dersler başarıyla takas edildi ({schedule_item.course.name} <-> {class_existing_lesson.course.name})."
                else:
                    schedule_item.time_slot = target_slot
                    schedule_item.save()
                    msg = f"Ders {target_day} {target_hour}. saate taşındı."

            updated_schedules = Schedule.objects.select_related('school_class', 'course', 'teacher', 'classroom', 'time_slot').all()
            serializer = ScheduleSerializer(updated_schedules, many=True)
            return Response({'message': msg, 'schedule': serializer.data}, status=status.HTTP_200_OK)

        except Schedule.DoesNotExist:
            return Response({'error': 'Belirtilen ders kaydı bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Ders taşıma hatası: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class GenerateScheduleView(APIView):
    def post(self, request):
        try:
            classrooms = list(Classroom.objects.all())
            time_slots = list(TimeSlot.objects.all())
            raw_requirements = CourseRequirement.objects.all()

            if not classrooms or not time_slots or not raw_requirements.exists():
                return Response(
                    {"error": "Classrooms, Time Slots, and Course Requirements must be defined before generating a schedule."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            solved_schedule = generate_schedule(raw_requirements, classrooms, time_slots)
            
            if solved_schedule is None:
                return Response(
                    {"error": "No valid schedule could be generated with the given constraints."},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            
            with transaction.atomic():
                Schedule.objects.all().delete()
                Schedule.objects.bulk_create(solved_schedule)

            saved_schedules = Schedule.objects.select_related('school_class', 'course', 'teacher', 'classroom', 'time_slot').all()
            serializer = ScheduleSerializer(saved_schedules, many=True)
            return Response(
                {"message": "Schedule generated successfully.", "schedule": serializer.data}, 
                status=status.HTTP_201_CREATED
            )
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def schedule_interface(request):
    return render(request, 'interface.html')


class AIChatView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        user_message = request.data.get('message', '').strip()
        history = request.data.get('history', [])
        
        if not user_message:
            return Response({"error": "Mesaj alanı boş olamaz."}, status=status.HTTP_400_BAD_REQUEST)
        
        reply = process_ai_chat(user_message, history)
        return Response({"reply": reply, "response": reply}, status=status.HTTP_200_OK)