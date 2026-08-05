from django.db import models
from .base_model import BaseModel

class TimeSlot(BaseModel):
    Days_Of_Week = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    day = models.CharField(max_length=10, choices=Days_Of_Week, verbose_name='Day of the Week')
    hour = models.IntegerField(verbose_name='Hours of the Day')
    start_time = models.TimeField(null=True, blank=True, verbose_name='Start Time')
    end_time = models.TimeField(null=True, blank=True, verbose_name='End Time')

    class Meta:
        unique_together = ('day', 'hour')

    @property
    def time_range_str(self):
        if self.start_time and self.end_time:
            return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        return f"{self.hour}. Saat"

    def __str__(self):
        return f"{self.get_day_display()} - {self.hour} ({self.time_range_str})"
