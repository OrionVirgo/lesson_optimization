from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TeacherViewSet,
    SchoolClassViewSet,
    CourseViewSet,
    ClassroomViewSet,
    TimeSlotViewSet,
    CourseRequirementViewSet,
    ScheduleViewSet,
    GenerateScheduleView,
    schedule_interface,
    AIChatView
)

router = DefaultRouter()
router.register('teachers', TeacherViewSet, basename='teacher')
router.register('school-classes', SchoolClassViewSet, basename='schoolclass')
router.register('courses', CourseViewSet, basename='course')
router.register('classrooms', ClassroomViewSet, basename='classroom')
router.register('time-slots', TimeSlotViewSet, basename='timeslot')
router.register('course-requirements', CourseRequirementViewSet, basename='courserequirement')
router.register('schedules', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('generate-schedule/', GenerateScheduleView.as_view(), name='generate-schedule'),
    path('ai/chat/', AIChatView.as_view(), name='ai-chat'),
    path('ai-chat/', AIChatView.as_view(), name='ai-chat-direct'),
    path('schedule/view/', schedule_interface, name='schedule_interface'),
    path('', include(router.urls)),
]