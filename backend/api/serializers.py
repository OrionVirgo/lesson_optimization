from rest_framework import serializers
from .models import (
    Teacher,
    SchoolClass,
    Course,
    Classroom,
    TimeSlot,
    CourseRequirement,
    Schedule
)

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class SchoolClassSerializer(serializers.ModelSerializer):
    advisor = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), required=False, allow_null=True)
    advisor_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SchoolClass
        fields = '__all__'

    def get_advisor_name(self, obj):
        if obj.advisor:
            prefix = f"{obj.advisor.academic_title} " if obj.advisor.academic_title else ""
            return f"{prefix}{obj.advisor.name}"
        return None

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'

class TimeSlotSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display', read_only=True)
    
    class Meta:
        model = TimeSlot
        fields = '__all__'

class CourseRequirementSerializer(serializers.ModelSerializer):
    school_class_name = serializers.CharField(source='school_class.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)

    class Meta:
        model = CourseRequirement
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    school_class_name = serializers.CharField(source='school_class.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    day = serializers.CharField(source='time_slot.day', read_only=True)
    hour = serializers.IntegerField(source='time_slot.hour', read_only=True)
    is_lab = serializers.BooleanField(source='classroom.is_lab', read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'