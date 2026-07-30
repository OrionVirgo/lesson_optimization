from django.db import models
from .base_model import BaseModel
from .teacher import Teacher


class SchoolClass(BaseModel):
    DEGREE_CHOICES = [
        ('Bachelor (B.Sc.)', 'Bachelor (B.Sc.)'),
        ('Master (M.Sc.)', 'Master (M.Sc.)'),
        ('Doctorate (Ph.D.)', 'Doctorate (Ph.D.)'),
        ('Associate (A.A.)', 'Associate (A.A.)'),
    ]

    YEAR_CHOICES = [
        ('Year 1 (Freshman)', 'Year 1 (Freshman)'),
        ('Year 2 (Sophomore)', 'Year 2 (Sophomore)'),
        ('Year 3 (Junior)', 'Year 3 (Junior)'),
        ('Year 4 (Senior)', 'Year 4 (Senior)'),
    ]

    name = models.CharField(max_length=100, verbose_name='Cohort / Section Name')
    degree_level = models.CharField(max_length=30, choices=DEGREE_CHOICES, default='Bachelor (B.Sc.)', verbose_name='Degree Level')
    academic_year = models.CharField(max_length=30, choices=YEAR_CHOICES, default='Year 1 (Freshman)', verbose_name='Academic Year')
    student_count = models.IntegerField(default=40, verbose_name='Student Count / Capacity')
    advisor = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='advised_classes', verbose_name='Academic Advisor')
    home_building = models.CharField(max_length=100, blank=True, null=True, verbose_name='Preferred Building / Campus')

    def __str__(self):
        return self.name
