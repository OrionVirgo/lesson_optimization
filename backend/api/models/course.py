from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='Course Name')
    is_lab_required = models.BooleanField(default=False, verbose_name='Lab Required')

    def __str__(self):
        return self.name
