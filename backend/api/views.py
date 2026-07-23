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

class SeedDataView(APIView):
    def post(self, request):
        with transaction.atomic():
            Schedule.objects.all().delete()
            CourseRequirement.objects.all().delete()
            Teacher.objects.all().delete()
            Course.objects.all().delete()
            Classroom.objects.all().delete()
            SchoolClass.objects.all().delete()
            TimeSlot.objects.all().delete()

            teachers_data = [
                {"name": "John Smith (Mathematics)", "off_day": "Friday"},
                {"name": "Alice Cooper (Physics)", "off_day": "Wednesday"},
                {"name": "Robert Taylor (Chemistry)", "off_day": "Monday"},
                {"name": "Emma Wilson (Biology)", "off_day": "Thursday"},
                {"name": "David Brown (Literature)", "off_day": "Tuesday"},
            ]
            teachers = [Teacher.objects.create(**t) for t in teachers_data]

            classes_data = ["Grade 9-A", "Grade 10-A", "Grade 11-A"]
            school_classes = [SchoolClass.objects.create(name=c) for c in classes_data]

            courses_data = [
                {"name": "Mathematics", "is_lab_required": False},
                {"name": "Physics", "is_lab_required": True},
                {"name": "Chemistry", "is_lab_required": True},
                {"name": "Biology", "is_lab_required": False},
                {"name": "Literature", "is_lab_required": False},
            ]
            courses = [Course.objects.create(**c) for c in courses_data]

            classrooms_data = [
                {"name": "Classroom 101", "is_lab": False},
                {"name": "Classroom 102", "is_lab": False},
                {"name": "Science Lab", "is_lab": True},
                {"name": "Chemistry Lab", "is_lab": True},
            ]
            classrooms = [Classroom.objects.create(**cr) for cr in classrooms_data]

            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            time_slots = []
            for d in days:
                for h in range(1, 7):
                    ts = TimeSlot.objects.create(day=d, hour=h)
                    time_slots.append(ts)

            requirements_data = [
                {"school_class": school_classes[0], "course": courses[0], "teacher": teachers[0], "weekly_hours": 4},
                {"school_class": school_classes[0], "course": courses[1], "teacher": teachers[1], "weekly_hours": 3},
                {"school_class": school_classes[0], "course": courses[2], "teacher": teachers[2], "weekly_hours": 2},
                {"school_class": school_classes[0], "course": courses[3], "teacher": teachers[3], "weekly_hours": 2},
                {"school_class": school_classes[0], "course": courses[4], "teacher": teachers[4], "weekly_hours": 3},

                {"school_class": school_classes[1], "course": courses[0], "teacher": teachers[0], "weekly_hours": 4},
                {"school_class": school_classes[1], "course": courses[1], "teacher": teachers[1], "weekly_hours": 3},
                {"school_class": school_classes[1], "course": courses[2], "teacher": teachers[2], "weekly_hours": 3},

                {"school_class": school_classes[2], "course": courses[0], "teacher": teachers[0], "weekly_hours": 4},
                {"school_class": school_classes[2], "course": courses[3], "teacher": teachers[3], "weekly_hours": 3},
            ]
            for req in requirements_data:
                CourseRequirement.objects.create(**req)

        return Response({"message": "Sample data seeded successfully."}, status=status.HTTP_201_CREATED)

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
    return render(request, 'api/interface.html')