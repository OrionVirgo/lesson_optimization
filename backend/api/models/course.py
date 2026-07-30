from django.db import models
from .base_model import BaseModel


class Course(BaseModel):
    COURSE_TYPES = [
        ('Compulsory', 'Compulsory'),
        ('Elective', 'Elective'),
        ('General Requirement', 'General Requirement'),
    ]

    code = models.CharField(max_length=30, blank=True, null=True, verbose_name='Course Code')
    name = models.CharField(max_length=100, verbose_name='Course Title')
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name='Faculty / Department')
    credits = models.IntegerField(default=6, verbose_name='ECTS Credits')
    course_type = models.CharField(max_length=30, choices=COURSE_TYPES, default='Compulsory', verbose_name='Course Type')
    max_block_hours = models.IntegerField(default=2, verbose_name='Max Block Hours')
    is_lab_required = models.BooleanField(default=False, verbose_name='Requires Laboratory Facility')

    def __str__(self):
        return f"{self.code} - {self.name}" if self.code else self.name
