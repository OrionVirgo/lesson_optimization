from django.db import models

class Teacher(models.Model):
    Days_Of_Week = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    name = models.CharField(max_length=50,verbose_name='Teacher Name')
    off_day = models.CharField(max_length=10, choices= Days_Of_Week, verbose_name ='Off Day')

    def __str__(self):
        return self.name
    
class SchoolClass(models.Model):
    name=models.CharField(max_length=50, verbose_name='Class Name')

    def __str__(self):
        return self.name

class Course(models.Model):
    name= models.CharField(max_length=50, verbose_name='Course Name')
    is_lab_required = models.BooleanField(default=False, verbose_name='Lab Required')

    def __str__(self):
        return self.name

class Classroom(models.Model):
    name=models.CharField(max_length=50, verbose_name= 'Classroom Name')
    is_lab = models.BooleanField(default=False, verbose_name='Is Lab Classroom')

    def __str__(self):  
        return self.name
    
class TimeSlot(models.Model):
    Days_Of_Week = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    day =models.CharField(max_length = 10, choices = Days_Of_Week, verbose_name = 'Day of the Week')
    hour = models.IntegerField(verbose_name='Hours of the Day')

    class Meta:
        unique_together = ('day', 'hour')

    def __str__(self):
        return f"{self.get_day_display()} - {self.hour}"
    
class CourseRequirement(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete = models.CASCADE ,verbose_name ='School Class')
    course = models.ForeignKey(Course, on_delete= models.CASCADE, verbose_name = 'Course')
    weekly_hours = models.IntegerField(verbose_name='Weekly Hours')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Teacher')
    
    def __str__(self):
        return f"{self.school_class.name} - {self.course.name} - {self.teacher.name} ({self.weekly_hours} hour)"
    
class Schedule(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, verbose_name='School Class')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Teacher')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='Classroom')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, verbose_name='Time Slot')

    def __str__(self):
        return f"{self.school_class.name} - {self.course.name} - {self.teacher.name} - {self.classroom.name} - {self.time_slot}"