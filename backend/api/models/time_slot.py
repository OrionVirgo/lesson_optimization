from django.db import models

class TimeSlot(models.Model):
    Days_Of_Week = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    day = models.CharField(max_length=10, choices=Days_Of_Week, verbose_name='Day of the Week')
    hour = models.IntegerField(verbose_name='Hours of the Day')

    class Meta:
        unique_together = ('day', 'hour')

    def __str__(self):
        return f"{self.get_day_display()} - {self.hour}"
