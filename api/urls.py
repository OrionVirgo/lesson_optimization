from django.urls import path
from .views import GenerateScheduleView, schedule_interface   

urlpatterns = [
    path('generate-schedule/', GenerateScheduleView.as_view(), name='generate-schedule'),
    path('schedule/view/', schedule_interface, name='schedule_interface'),
]

