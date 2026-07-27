from django.db import models
from .base_model import BaseModel

class Classroom(BaseModel):
    name = models.CharField(max_length=50, verbose_name='Classroom Name')
    is_lab = models.BooleanField(default=False, verbose_name='Is Lab Classroom')

    def __str__(self):
        return self.name
