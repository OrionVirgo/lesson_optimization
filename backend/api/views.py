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

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer

class CourseRequirementViewSet(viewsets.ModelViewSet):
    queryset = CourseRequirement.objects.all()
    serializer_class = CourseRequirementSerializer

class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.select_related('school_class', 'course', 'teacher', 'classroom', 'time_slot').all()
    serializer_class = ScheduleSerializer

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