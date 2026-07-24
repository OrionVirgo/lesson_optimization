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
    name = models.CharField(max_length=50, verbose_name='Teacher Name')
    off_day = models.CharField(max_length=10, choices=Days_Of_Week, verbose_name='Off Day')

    def __str__(self):
        return self.name
