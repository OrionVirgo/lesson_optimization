from django.db import models

class Classroom(models.Model):
    name = models.CharField(max_length=50, verbose_name='Classroom Name')
    is_lab = models.BooleanField(default=False, verbose_name='Is Lab Classroom')

    def __str__(self):  
        return self.name
