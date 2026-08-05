from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from api.models import (
    Teacher,
    SchoolClass,
    Course,
    Classroom,
    TimeSlot,
    CourseRequirement,
    Schedule
)
from api.scheduler import generate_schedule

User = get_user_model()

class SchedulerTests(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name="Ahmet Yılmaz", off_day="Friday")
        self.school_class = SchoolClass.objects.create(name="10-A")
        self.course_normal = Course.objects.create(name="Matematik", is_lab_required=False)
        self.course_lab = Course.objects.create(name="Fizik Lab", is_lab_required=True)
        self.classroom_normal = Classroom.objects.create(name="Derslik 101", is_lab=False)
        self.classroom_lab = Classroom.objects.create(name="Fizik Laboratuvarı", is_lab=True)
        self.time_slot_1 = TimeSlot.objects.create(day="Monday", hour=1)
        self.time_slot_2 = TimeSlot.objects.create(day="Monday", hour=2)
        self.time_slot_friday = TimeSlot.objects.create(day="Friday", hour=1)

    def test_model_creation(self):
        self.assertEqual(Teacher.objects.count(), 1)
        self.assertEqual(SchoolClass.objects.count(), 1)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Classroom.objects.count(), 2)
        self.assertEqual(TimeSlot.objects.count(), 3)

    def test_generate_schedule_success(self):
        req = CourseRequirement.objects.create(
            school_class=self.school_class,
            course=self.course_normal,
            teacher=self.teacher,
            weekly_hours=2
        )
        classrooms = [self.classroom_normal]
        time_slots = [self.time_slot_1, self.time_slot_2]

        result = generate_schedule([req], classrooms, time_slots)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].teacher, self.teacher)
        self.assertEqual(result[0].school_class, self.school_class)
        self.assertEqual(result[0].classroom, self.classroom_normal)

    def test_generate_schedule_respects_teacher_off_day(self):
        req = CourseRequirement.objects.create(
            school_class=self.school_class,
            course=self.course_normal,
            teacher=self.teacher,
            weekly_hours=1
        )
        classrooms = [self.classroom_normal]
        time_slots = [self.time_slot_friday]  # Teacher off day is Friday

        result = generate_schedule([req], classrooms, time_slots)
        self.assertIsNone(result)

class APIEndpointsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = Teacher.objects.create(name="Mehmet Öz", off_day="Wednesday")
        self.school_class = SchoolClass.objects.create(name="11-B")
        self.course = Course.objects.create(name="Kimya", is_lab_required=False)
        self.classroom = Classroom.objects.create(name="Derslik 202", is_lab=False)
        self.time_slot = TimeSlot.objects.create(day="Tuesday", hour=1)

    def test_teacher_api(self):
        response = self.client.get('/api/teachers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Mehmet Öz")

    def test_auth_login_create_and_authenticate(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'Password123!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        access_token = response.data['access']

        # Test authenticated me endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        me_response = self.client.get('/api/auth/me/')
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(me_response.data['username'], 'testuser')

    def test_generate_schedule_api_endpoint(self):
        CourseRequirement.objects.create(
            school_class=self.school_class,
            course=self.course,
            teacher=self.teacher,
            weekly_hours=1
        )
        response = self.client.post('/api/generate-schedule/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Schedule.objects.count(), 1)

    def test_ai_chat_api_endpoint(self):
        response = self.client.post('/api/ai/chat/', {
            'message': 'Sistemde kaç öğretmen var?'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('reply', response.data)

    def test_move_lesson_api_endpoint(self):
        schedule = Schedule.objects.create(
            school_class=self.school_class,
            course=self.course,
            teacher=self.teacher,
            classroom=self.classroom,
            time_slot=self.time_slot
        )
        target_slot = TimeSlot.objects.create(day="Tuesday", hour=2)

        response = self.client.post('/api/schedules/move-lesson/', {
            'schedule_id': schedule.id,
            'target_day': 'Tuesday',
            'target_hour': 2
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schedule.refresh_from_db()
        self.assertEqual(schedule.time_slot.id, target_slot.id)

