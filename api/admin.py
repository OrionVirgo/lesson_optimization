from django.contrib import admin
from .models import Teacher, SchoolClass, Course, Classroom, TimeSlot, CourseRequirement, Schedule


admin.site.register(Teacher)
admin.site.register(SchoolClass)
admin.site.register(Course)
admin.site.register(Classroom)
admin.site.register(TimeSlot)
admin.site.register(CourseRequirement)
admin.site.register(Schedule)