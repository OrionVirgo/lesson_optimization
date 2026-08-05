import { createRouter, createWebHistory } from 'vue-router'
import TimetableView from '../views/TimetableView.vue'
import TeachersView from '../views/TeachersView.vue'
import ClassesView from '../views/ClassesView.vue'
import ClassroomsView from '../views/ClassroomsView.vue'
import CoursesView from '../views/CoursesView.vue'
import TimeSlotsView from '../views/TimeSlotsView.vue'
import CourseRequirementsView from '../views/CourseRequirementsView.vue'

const routes = [
  { path: '/', name: 'Timetable', component: TimetableView },
  { path: '/teachers', name: 'Teachers', component: TeachersView },
  { path: '/classes', name: 'Classes', component: ClassesView },
  { path: '/classrooms', name: 'Classrooms', component: ClassroomsView },
  { path: '/courses', name: 'Courses', component: CoursesView },
  { path: '/timeslots', name: 'TimeSlots', component: TimeSlotsView },
  { path: '/requirements', name: 'Requirements', component: CourseRequirementsView },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
