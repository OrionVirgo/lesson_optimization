from django.db import models
from .base_model import BaseModel


class Classroom(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Room / Hall Name')
    capacity = models.IntegerField(default=50, verbose_name='Seating Capacity')
    is_lab = models.BooleanField(default=False, verbose_name='Is Laboratory Facility?')

    def __str__(self):
        return self.name
