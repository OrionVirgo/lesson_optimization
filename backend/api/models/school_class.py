from django.db import models
from .base_model import BaseModel

class SchoolClass(BaseModel):
    name = models.CharField(max_length=50, verbose_name='Class Name')

    def __str__(self):
        return self.name
