import axios from 'axios'

const API_BASE_URL = '/api'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request Interceptor to add JWT Auth Token if present
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('jwt_access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interfaces
export interface Teacher {
  id?: number
  name: string
  branch?: string
  academic_title?: string
  off_day?: string
  phone?: string
  email?: string
}

export interface SchoolClass {
  id?: number
  name: string
  grade_level?: number
  student_count?: number
}

export interface Classroom {
  id?: number
  name: string
  building_wing?: string
  capacity?: number
  is_lab: boolean
}

export interface Course {
  id?: number
  code?: string
  name: string
  is_lab_required: boolean
}

export interface TimeSlot {
  id?: number
  day: string
  hour: number
  time_range_str?: string
  start_time?: string
  end_time?: string
}

export interface CourseRequirement {
  id?: number
  school_class: number
  school_class_name?: string
  course: number
  course_name?: string
  teacher: number
  teacher_name?: string
  weekly_hours: number
}

export interface ScheduleEntry {
  id: number
  school_class: SchoolClass | number
  school_class_name?: string
  course: Course | number
  course_name?: string
  teacher: Teacher | number
  teacher_name?: string
  classroom: Classroom | number
  classroom_name?: string
  time_slot: TimeSlot | number
  day?: string
  hour?: number
}

// API Services
export const TeacherService = {
  getAll: () => apiClient.get<Teacher[]>('/teachers/').then(r => r.data),
  create: (data: Teacher) => apiClient.post<Teacher>('/teachers/', data).then(r => r.data),
  update: (id: number, data: Teacher) => apiClient.put<Teacher>(`/teachers/${id}/`, data).then(r => r.data),
  delete: (id: number) => apiClient.delete(`/teachers/${id}/`)
}

export const ClassService = {
  getAll: () => apiClient.get<SchoolClass[]>('/school-classes/').then(r => r.data),
  create: (data: SchoolClass) => apiClient.post<SchoolClass>('/school-classes/', data).then(r => r.data),
  update: (id: number, data: SchoolClass) => apiClient.put<SchoolClass>(`/school-classes/${id}/`, data).then(r => r.data),
  delete: (id: number) => apiClient.delete(`/school-classes/${id}/`)
}

export const ClassroomService = {
  getAll: () => apiClient.get<Classroom[]>('/classrooms/').then(r => r.data),
  create: (data: Classroom) => apiClient.post<Classroom>('/classrooms/', data).then(r => r.data),
  update: (id: number, data: Classroom) => apiClient.put<Classroom>(`/classrooms/${id}/`, data).then(r => r.data),
  delete: (id: number) => apiClient.delete(`/classrooms/${id}/`)
}

export const CourseService = {
  getAll: () => apiClient.get<Course[]>('/courses/').then(r => r.data),
  create: (data: Course) => apiClient.post<Course>('/courses/', data).then(r => r.data),
  update: (id: number, data: Course) => apiClient.put<Course>(`/courses/${id}/`, data).then(r => r.data),
  delete: (id: number) => apiClient.delete(`/courses/${id}/`)
}

export const TimeSlotService = {
  getAll: () => apiClient.get<TimeSlot[]>('/time-slots/').then(r => r.data),
  create: (data: TimeSlot) => apiClient.post<TimeSlot>('/time-slots/', data).then(r => r.data),
  update: (id: number, data: TimeSlot) => apiClient.put<TimeSlot>(`/time-slots/${id}/`, data).then(r => r.data),
  delete: (id: number) => apiClient.delete(`/time-slots/${id}/`)
}

export const RequirementService = {
  getAll: () => apiClient.get<CourseRequirement[]>('/course-requirements/').then(r => r.data),
  create: (data: CourseRequirement) => apiClient.post<CourseRequirement>('/course-requirements/', data).then(r => r.data),
  update: (id: number, data: CourseRequirement) => apiClient.put<CourseRequirement>(`/course-requirements/${id}/`, data).then(r => r.data),
  delete: (id: number) => apiClient.delete(`/course-requirements/${id}/`)
}

export const ScheduleService = {
  getAll: () => apiClient.get<ScheduleEntry[]>('/schedules/').then(r => r.data),
  generate: () => apiClient.post<{ message: string; count: number }>('/generate-schedule/').then(r => r.data)
}

export const AIChatService = {
  sendMessage: (message: string, history?: any[]) => 
    apiClient.post<{ response: string }>('/ai-chat/', { message, history }).then(r => r.data)
}
