from django.db import models
from .base_model import BaseModel


class Teacher(BaseModel):
    Days_Of_Week = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]

    TITLE_CHOICES = [
        ('Prof. Dr.', 'Prof. Dr.'),
        ('Assoc. Prof. Dr.', 'Assoc. Prof. Dr.'),
        ('Asst. Prof. Dr.', 'Asst. Prof. Dr.'),
        ('Lecturer', 'Lecturer'),
        ('Research Asst.', 'Research Asst.'),
        ('Teacher', 'Teacher'),
    ]

    academic_title = models.CharField(max_length=30, choices=TITLE_CHOICES, default='Prof. Dr.', verbose_name='Academic Title')
    name = models.CharField(max_length=100, verbose_name='Full Name')
    email = models.EmailField(blank=True, null=True, verbose_name='Email Address')
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name='Phone Number')
    branch = models.CharField(max_length=100, blank=True, null=True, verbose_name='Department / Field')
    office_room = models.CharField(max_length=30, blank=True, null=True, verbose_name='Office Room Number')
    off_day = models.CharField(max_length=10, choices=Days_Of_Week, default='Monday', verbose_name='Off Day')
    max_daily_hours = models.IntegerField(default=6, verbose_name='Max Daily Teaching Hours')

    def __str__(self):
        title_prefix = f"{self.academic_title} " if self.academic_title else ""
        return f"{title_prefix}{self.name}"
 