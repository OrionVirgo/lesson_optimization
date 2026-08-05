export default {
  app: {
    title: 'Lesson Scheduling Optimization Portal',
    subtitle: 'Conflict-free Schedule Generator & Gemini AI Assistant'
  },
  nav: {
    dashboard: 'Timetable',
    teachers: 'Teachers',
    classes: 'School Classes',
    classrooms: 'Classrooms',
    courses: 'Courses',
    timeslots: 'Time Slots',
    requirements: 'Course Requirements',
    aiAssistant: 'AI Assistant'
  },
  actions: {
    add: 'Add New',
    edit: 'Edit',
    delete: 'Delete',
    save: 'Save',
    cancel: 'Cancel',
    close: 'Close',
    generateSchedule: 'Auto-Generate Schedule',
    generating: 'Calculating Optimization...',
    print: 'Print Schedule / PDF',
    filter: 'Filter',
    all: 'All',
    search: 'Search...',
    confirm: 'Confirm'
  },
  timetable: {
    title: 'Weekly Timetable Matrix',
    selectClass: 'Select Class:',
    selectTeacher: 'Select Teacher:',
    allClasses: 'All Classes',
    allTeachers: 'All Teachers',
    emptySlot: 'Empty Slot',
    conflictWarning: 'Potential Conflict Detected!',
    labRequired: 'Lab Required',
    offDay: 'Off Day',
    generatedSuccess: 'Schedule successfully generated without conflicts!',
    generatedError: 'Could not generate a valid schedule with current constraints.'
  },
  teachers: {
    title: 'Teacher Management',
    name: 'Full Name',
    titleBranch: 'Title / Branch',
    offDay: 'Off Day',
    phone: 'Phone',
    email: 'Email',
    maxHours: 'Max Daily Hours',
    actions: 'Actions'
  },
  classes: {
    title: 'School Class Management',
    name: 'Class Name',
    gradeLevel: 'Grade Level',
    studentCount: 'Student Count'
  },
  classrooms: {
    title: 'Classroom & Lab Management',
    name: 'Classroom Name',
    building: 'Building / Wing',
    capacity: 'Capacity',
    isLab: 'Is Laboratory?'
  },
  courses: {
    title: 'Course Catalog',
    code: 'Course Code',
    name: 'Course Name',
    isLabRequired: 'Lab Required?'
  },
  timeslots: {
    title: 'Time Slots',
    day: 'Day',
    hour: 'Hour / Period',
    timeRange: 'Time Range'
  },
  requirements: {
    title: 'Course Allocations & Requirements',
    schoolClass: 'Target Class',
    course: 'Assigned Course',
    teacher: 'Assigned Teacher',
    weeklyHours: 'Weekly Hours'
  },
  ai: {
    title: 'Gemini AI Assistant',
    placeholder: 'Ask about schedule conflicts, teacher availability, or empty rooms...',
    quickQuestions: 'Quick Questions:',
    q1: 'Are there any schedule bottlenecks?',
    q2: 'List empty classrooms',
    q3: 'Summarize teacher workloads',
    sending: 'Thinking...'
  }
}
