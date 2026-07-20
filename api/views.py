from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Schedule, Classroom ,TimeSlot, CourseRequirement
from .scheduler import generate_schedule

class GenerateScheduleView(APIView):
    def post(self, request):
        try:
            classrooms =list(Classroom.objects.all())
            time_slots = list(TimeSlot.objects.all())
            raw_requirements = CourseRequirement.objects.all()

            if not classrooms or not time_slots or not raw_requirements.exists():
                return Response({"error": "Classrooms, Time Slots, and Course Requirements must be defined before generating a schedule."},
                                 status=status.HTTP_400_BAD_REQUEST)

            Schedule.objects.all().delete()

            solved_schedule = generate_schedule(raw_requirements, classrooms, time_slots)
            
            if solved_schedule is None:
                return Response({"error": "No valid schedule could be generated with the given constraints."},
                                 status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            Schedule.objects.bulk_create(solved_schedule)

            response_data =[]
            for item in solved_schedule:
                response_data.append({
                    "school_class": item.school_class.name,
                    "course": item.course.name,
                    "teacher": item.teacher.name,
                    "classroom": item.classroom.name,
                    "day": item.time_slot.day,
                    "hour": item.time_slot.hour
                })
            return Response({"message": "Schedule generated successfully.", "schedule": response_data}, 
                            status=status.HTTP_201_CREATED)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": "An unexpected error occurred: " + str(e)},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

from django.shortcuts import render

def schedule_interface(request):
    # Bu view hiçbir veritabanı işlemi yapmaz, sadece HTML sayfasını yükler
    return render(request, 'api/interface.html')