from django.db import models
from .base_model import BaseModel
from .school_class import SchoolClass
from .course import Course
from .teacher import Teacher
from .classroom import Classroom
from .time_slot import TimeSlot

class Schedule(BaseModel):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, verbose_name='School Class')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Teacher')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='Classroom')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, verbose_name='Time Slot')

    def __str__(self):
        return f"{self.school_class.name} - {self.course.name} - {self.teacher.name} - {self.classroom.name} - {self.time_slot}"
