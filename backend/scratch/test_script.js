
        const { createApp, ref, reactive, computed, onMounted } = Vue;

        // Vue 3 DeleteModal Component (Using explicit props and emits)
        const DeleteModal = {
            name: 'DeleteModal',
            props: {
                show: { type: Boolean, default: false },
                title: { type: String, default: 'Confirm Deletion' },
                message: { type: String, default: '' },
                itemId: { type: [Number, String], default: null },
                endpoint: { type: String, default: '' },
                t: { type: Function, required: true }
            },
            emits: ['close', 'confirm'],
            template: `
                <div v-if="show" class="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
                    <div class="glass-card rounded-2xl p-6 w-full max-w-md border border-rose-900/50 shadow-2xl flex flex-col gap-4">
                        <div class="flex items-center gap-3 text-rose-400">
                            <div class="w-10 h-10 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center">
                                <i class="fa-solid fa-triangle-exclamation text-lg"></i>
                            </div>
                            <h3 class="text-lg font-bold text-white">{{ title }}</h3>
                        </div>
                        
                        <p class="text-sm text-slate-300 leading-relaxed">
                            {{ message }}
                        </p>

                        <div class="flex justify-end gap-2 mt-2 pt-3 border-t border-slate-800">
                            <button type="button" @click="$emit('close')" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-semibold">
                                {{ t('cancel') }}
                            </button>
                            <button type="button" @click="$emit('confirm', { endpoint, id: itemId })" class="px-5 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-sm font-semibold shadow-lg shadow-rose-600/20">
                                {{ t('delete') }}
                            </button>
                        </div>
                    </div>
                </div>
            `
        };
{% endverbatim %}

        const app = createApp({
            components: {
                DeleteModal
            },
            setup() {
                const API_BASE = window.location.origin && window.location.origin.startsWith('http')
                    ? `${window.location.origin}/api`
                    : 'http://127.0.0.1:8000/api';
                const dayKeys = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

                // Vue 3 Reactive i18n
                const currentLang = ref(localStorage.getItem('app_lang') || 'tr');

                const translations = {
                    tr: {
                        app_title: "Ders Programı",
                        app_title_highlight: "Optimizasyonu",
                        app_subtitle: "Akıllı ve Çakışmasız Ders Programı Oluşturucu",
                        user_auth: "Kullanıcı Girişi",
                        welcome: "Hoş geldiniz,",
                        login: "Giriş Yap",
                        log_out: "Çıkış Yap",
                        username: "Kullanıcı Adı",
                        password: "Şifre",
                        enter_username: "Kullanıcı adınızı girin",
                        enter_password: "Şifrenizi girin",
                        generate_schedule: "Program Oluştur",
                        print_timetable: "Yazdır",

                        tab_timetable: "Haftalık Ders Programı",
                        tab_teachers: "Öğretmenler",
                        tab_classes: "Sınıflar & Derslikler",
                        tab_courses: "Dersler & Atamalar",
                        tab_timeslots: "Zaman Dilimleri",

                        select_class: "Sınıf Seçin:",
                        schedule_matrix_title: "Haftalık Ders Programı Tablosu",
                        overview_mon_fri: "Pazartesi - Cuma Haftalık Genel Bakış",
                        lecture: "Teorik Ders",
                        laboratory: "Laboratuvar",
                        hour: "Saat",
                        hour_num: "Saat {num}",
                        empty: "Boş",

                        day_monday: "Pazartesi",
                        day_tuesday: "Salı",
                        day_wednesday: "Çarşamba",
                        day_thursday: "Perşembe",
                        day_friday: "Cuma",

                        teacher_mgmt_title: "Öğretmen Yönetimi",
                        teacher_mgmt_subtitle: "Öğretmen kadrosunu ve haftalık izin günlerini yönetin",
                        add_teacher: "Yeni Öğretmen Ekle",
                        teacher_name: "Öğretmen Adı",
                        branch: "Branş",
                        off_day: "İzin Günü",
                        actions: "İşlemler",
                        no_teachers: "Henüz öğretmen eklenmedi.",

                        classes_mgmt_title: "Sınıf ve Derslik Yönetimi",
                        classes_mgmt_subtitle: "Öğrenci sınıflarını ve mevcut fiziksel derslikleri yapılandırın",
                        school_classes: "Okul Sınıfları",
                        classrooms: "Fiziksel Derslikler",
                        add_class: "Yeni Sınıf Ekle",
                        add_classroom: "Yeni Derslik Ekle",
                        class_name: "Sınıf Adı",
                        grade_level: "Sınıf Seviyesi",
                        capacity: "Kapasite",
                        is_lab: "Laboratuvar Donanımlı mı?",
                        yes: "Evet",
                        no: "Hayır",
                        no_classes: "Henüz sınıf eklenmedi.",
                        no_classrooms: "Henüz derslik eklenmedi.",

                        courses_mgmt_title: "Dersler ve Atamalar",
                        courses_mgmt_subtitle: "Ders tanımları ve haftalık sınıf atama gereksinimleri",
                        course_list: "Ders Listesi",
                        course_assignments: "Sınıf Ders Atamaları",
                        add_course: "Yeni Ders Ekle",
                        add_assignment: "Yeni Atama Ekle",
                        course_name: "Ders Adı",
                        course_code: "Ders Kodu",
                        weekly_hours: "Haftalık Saat",
                        requires_lab: "Laboratuvar Gerektirir mi?",
                        assigned_class: "Atanan Sınıf",
                        assigned_teacher: "Atanan Öğretmen",
                        no_courses: "Henüz ders eklenmedi.",
                        no_assignments: "Henüz ders ataması yapılmadı.",

                        timeslots_mgmt_title: "Zaman Dilimleri",
                        timeslots_mgmt_subtitle: "Sistemde tanımlı haftalık ders saatleri",
                        generate_default_slots: "Varsayılan Dilimleri Oluştur (40 Saat)",
                        day: "Gün",
                        no_timeslots: "Henüz zaman dilimi eklenmedi.",

                        cancel: "İptal",
                        save: "Kaydet",
                        delete: "Sil",
                        confirm_delete_title: "Silmeyi Onayla",
                        confirm_delete_msg: "Bu kaydı silmek istediğinizden emin misiniz?"
                    },
                    en: {
                        app_title: "Schedule",
                        app_title_highlight: "Optimization",
                        app_subtitle: "Intelligent Conflict-Free Timetable Generator",
                        user_auth: "User Authentication",
                        welcome: "Welcome,",
                        login: "Log In",
                        log_out: "Log Out",
                        username: "Username",
                        password: "Password",
                        enter_username: "Enter username",
                        enter_password: "Enter password",
                        generate_schedule: "Generate Schedule",
                        print_timetable: "Print",

                        tab_timetable: "Weekly Schedule",
                        tab_teachers: "Teachers",
                        tab_classes: "Classes & Rooms",
                        tab_courses: "Courses & Assignments",
                        tab_timeslots: "Time Slots",

                        select_class: "Select Class:",
                        schedule_matrix_title: "Weekly Schedule Matrix",
                        overview_mon_fri: "Monday - Friday Weekly Overview",
                        lecture: "Lecture",
                        laboratory: "Laboratory",
                        hour: "Hour",
                        hour_num: "Hour {num}",
                        empty: "Empty",

                        day_monday: "Monday",
                        day_tuesday: "Tuesday",
                        day_wednesday: "Wednesday",
                        day_thursday: "Thursday",
                        day_friday: "Friday",

                        teacher_mgmt_title: "Teacher Management",
                        teacher_mgmt_subtitle: "Manage teaching staff and weekly off-days",
                        add_teacher: "Add New Teacher",
                        teacher_name: "Teacher Name",
                        branch: "Branch",
                        off_day: "Off-Day",
                        actions: "Actions",
                        no_teachers: "No teachers added yet.",

                        classes_mgmt_title: "Class & Classroom Management",
                        classes_mgmt_subtitle: "Configure student grades and physical classrooms",
                        school_classes: "School Classes",
                        classrooms: "Physical Classrooms",
                        add_class: "Add New Class",
                        add_classroom: "Add New Classroom",
                        class_name: "Class Name",
                        grade_level: "Grade Level",
                        capacity: "Capacity",
                        is_lab: "Is Lab Equipped?",
                        yes: "Yes",
                        no: "No",
                        no_classes: "No classes added yet.",
                        no_classrooms: "No classrooms added yet.",

                        courses_mgmt_title: "Courses & Assignments",
                        courses_mgmt_subtitle: "Manage course catalog and weekly class allocations",
                        course_list: "Course List",
                        course_assignments: "Class Course Assignments",
                        add_course: "Add New Course",
                        add_assignment: "Add New Assignment",
                        course_name: "Course Name",
                        course_code: "Course Code",
                        weekly_hours: "Weekly Hours",
                        requires_lab: "Requires Laboratory?",
                        assigned_class: "Assigned Class",
                        assigned_teacher: "Assigned Teacher",
                        no_courses: "No courses added yet.",
                        no_assignments: "No course assignments created yet.",

                        timeslots_mgmt_title: "Time Slots",
                        timeslots_mgmt_subtitle: "Weekly schedule time slots and period definitions",
                        generate_default_slots: "Generate Default Slots (40 Hours)",
                        day: "Day",
                        no_timeslots: "No time slots added yet.",

                        cancel: "Cancel",
                        save: "Save",
                        delete: "Delete",
                        confirm_delete_title: "Confirm Delete",
                        confirm_delete_msg: "Are you sure you want to delete this record?"
                    }
                };

                const t = (key, params = {}) => {
                    let text = translations[currentLang.value]?.[key] || translations['tr']?.[key] || key;
                    if (params) {
                        Object.keys(params).forEach(p => {
                            text = text.replace(new RegExp(`\\{${p}\\}`, 'g'), params[p]);
                        });
                    }
                    return text;
                };

                const setLanguage = (lang) => {
                    currentLang.value = lang;
                    localStorage.setItem('app_lang', lang);
                };

                const isLoggedIn = ref(false);
                const user = ref(null);
                const activeTab = ref('timetable');
                const activeModal = ref(null);
                const filterTargetClass = ref('');
                const toasts = ref([]);

                const loginForm = reactive({ username: '', password: '' });
                const loginError = ref('');

                const state = reactive({
                    teachers: [],
                    classes: [],
                    classrooms: [],
                    courses: [],
                    requirements: [],
                    timeslots: [],
                    schedules: []
                });

                const formTeacher = reactive({
                    academic_title: 'Prof. Dr.',
                    name: '',
                    email: '',
                    phone: '',
                    branch: '',
                    office_room: '',
                    off_day: 'Monday',
                    max_daily_hours: 6
                });
                const isEditTeacher = ref(false);
                const editingTeacherId = ref(null);
                const isEditClass = ref(false);
                const editingClassId = ref(null);
                const isEditClassroom = ref(false);
                const editingClassroomId = ref(null);
                const isEditCourse = ref(false);
                const editingCourseId = ref(null);
                const isEditReq = ref(false);
                const editingReqId = ref(null);

                const showDeleteModal = ref(false);
                const deleteTarget = reactive({
                    title: '',
                    message: '',
                    endpoint: '',
                    id: null
                });

                const formClass = reactive({
                    name: '',
                    degree_level: 'Bachelor (B.Sc.)',
                    academic_year: 'Year 1 (Freshman)',
                    student_count: 40,
                    advisor: '',
                    home_building: ''
                });

                const formClassroom = reactive({
                    name: '',
                    capacity: 50,
                    is_lab: false
                });

                const formCourse = reactive({
                    code: '',
                    name: '',
                    department: '',
                    credits: 6,
                    course_type: 'Compulsory',
                    max_block_hours: 2,
                    is_lab_required: false
                });

                const formReq = reactive({ school_class: '', course: '', teacher: '', weekly_hours: 2 });

                const getAuthHeaders = (extra = {}) => {
                    const token = localStorage.getItem('access_token');
                    const headers = { ...extra };
                    if (token) headers['Authorization'] = `Bearer ${token}`;
                    return headers;
                };

                const showToast = (message, type = 'info') => {
                    const id = Date.now() + Math.random();
                    toasts.value.push({ id, message, type });
                    setTimeout(() => {
                        toasts.value = toasts.value.filter(t => t.id !== id);
                    }, 4000);
                };

                const checkAuth = async () => {
                    const token = localStorage.getItem('access_token');
                    if (token) {
                        try {
                            const res = await axios.get(`${API_BASE}/auth/me/`, { headers: getAuthHeaders() });
                            user.value = res.data;
                            isLoggedIn.value = true;
                            loadAllData();
                            return;
                        } catch (e) {}
                    }
                    handleLogout(false);
                };

                const handleLogin = async () => {
                    loginError.value = '';
                    if (!loginForm.username || !loginForm.password) {
                        loginError.value = 'Please enter username and password.';
                        return;
                    }
                    try {
                        const res = await axios.post(`${API_BASE}/auth/login/`, loginForm);
                        const data = res.data;
                        localStorage.setItem('access_token', data.access);
                        localStorage.setItem('refresh_token', data.refresh);
                        showToast(`Welcome back, ${data.user.username}!`, 'success');
                        checkAuth();
                    } catch (e) {
                        loginError.value = e.response?.data?.error || 'Login failed.';
                    }
                };

                const handleLogout = (notify = true) => {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    isLoggedIn.value = false;
                    user.value = null;
                    if (notify) showToast('Logged out successfully.', 'info');
                };

                const loadAllData = async () => {
                    try {
                        const config = { headers: getAuthHeaders() };
                        const [tRes, clRes, crRes, coRes, reqRes, tsRes, schRes] = await Promise.all([
                            axios.get(`${API_BASE}/teachers/`, config),
                            axios.get(`${API_BASE}/school-classes/`, config),
                            axios.get(`${API_BASE}/classrooms/`, config),
                            axios.get(`${API_BASE}/courses/`, config),
                            axios.get(`${API_BASE}/course-requirements/`, config),
                            axios.get(`${API_BASE}/time-slots/`, config),
                            axios.get(`${API_BASE}/schedules/`, config)
                        ]);

                        state.teachers = tRes.data;
                        state.classes = clRes.data;
                        state.classrooms = crRes.data;
                        state.courses = coRes.data;
                        state.requirements = reqRes.data;
                        state.timeslots = tsRes.data;
                        state.schedules = schRes.data;

                        if (state.classes.length > 0 && !filterTargetClass.value) {
                            filterTargetClass.value = state.classes[0].name;
                        }
                    } catch (e) {
                        showToast('Error loading system data', 'error');
                    }
                };

                const parseError = (e) => {
                    if (!e.response?.data) return 'Network or server error occurred.';
                    const data = e.response.data;
                    if (typeof data === 'string') return data;
                    if (data.error) return data.error;
                    if (typeof data === 'object') {
                        const keys = Object.keys(data);
                        if (keys.length > 0) {
                            const field = keys[0];
                            const msg = Array.isArray(data[field]) ? data[field].join(', ') : data[field];
                            return `${field}: ${msg}`;
                        }
                    }
                    return 'Operation failed.';
                };

                const fetchPost = async (endpoint, data, successMsg) => {
                    try {
                        await axios.post(`${API_BASE}/${endpoint}/`, data, {
                            headers: getAuthHeaders()
                        });
                        showToast(successMsg, 'success');
                        closeModal();
                        loadAllData();
                    } catch (e) {
                        showToast(parseError(e), 'error');
                    }
                };

                const confirmDelete = (endpoint, id, itemName = 'this item') => {
                    deleteTarget.title = t('confirm_delete_title');
                    deleteTarget.message = `${t('confirm_delete_msg')} (${itemName})`;
                    deleteTarget.endpoint = endpoint;
                    deleteTarget.id = id;
                    showDeleteModal.value = true;
                };

                const handleConfirmDelete = async ({ endpoint, id }) => {
                    if (!endpoint || !id) return;
                    try {
                        await axios.delete(`${API_BASE}/${endpoint}/${id}/`, {
                            headers: getAuthHeaders()
                        });
                        showToast(t('delete') + ' successful.', 'success');
                        showDeleteModal.value = false;
                        loadAllData();
                    } catch (e) {
                        showToast(parseError(e), 'error');
                    }
                };

                const deleteItem = async (endpoint, id) => {
                    return confirmDelete(endpoint, id);
                };

                const resetTeacherForm = () => {
                    formTeacher.academic_title = 'Prof. Dr.';
                    formTeacher.name = '';
                    formTeacher.email = '';
                    formTeacher.phone = '';
                    formTeacher.branch = '';
                    formTeacher.office_room = '';
                    formTeacher.off_day = 'Monday';
                    formTeacher.max_daily_hours = 6;
                };

                const resetClassForm = () => {
                    formClass.name = '';
                    formClass.degree_level = 'Bachelor (B.Sc.)';
                    formClass.academic_year = 'Year 1 (Freshman)';
                    formClass.student_count = 40;
                    formClass.advisor = '';
                    formClass.home_building = '';
                };

                const resetClassroomForm = () => {
                    formClassroom.name = '';
                    formClassroom.capacity = 50;
                    formClassroom.is_lab = false;
                };

                const resetCourseForm = () => {
                    formCourse.code = '';
                    formCourse.name = '';
                    formCourse.department = '';
                    formCourse.credits = 6;
                    formCourse.course_type = 'Compulsory';
                    formCourse.max_block_hours = 2;
                    formCourse.is_lab_required = false;
                };

                const editTeacher = (teacher) => {
                    isEditTeacher.value = true;
                    editingTeacherId.value = teacher.id;
                    formTeacher.academic_title = teacher.academic_title || 'Prof. Dr.';
                    formTeacher.name = teacher.name || '';
                    formTeacher.email = teacher.email || '';
                    formTeacher.phone = teacher.phone || '';
                    formTeacher.branch = teacher.branch || '';
                    formTeacher.office_room = teacher.office_room || '';
                    formTeacher.off_day = teacher.off_day || 'Monday';
                    formTeacher.max_daily_hours = teacher.max_daily_hours || 6;
                    activeModal.value = 'teacher';
                };

                const editClass = (schoolClass) => {
                    isEditClass.value = true;
                    editingClassId.value = schoolClass.id;
                    formClass.name = schoolClass.name || '';
                    formClass.degree_level = schoolClass.degree_level || 'Bachelor (B.Sc.)';
                    formClass.academic_year = schoolClass.academic_year || 'Year 1 (Freshman)';
                    formClass.student_count = schoolClass.student_count || 40;
                    formClass.advisor = schoolClass.advisor || '';
                    formClass.home_building = schoolClass.home_building || '';
                    activeModal.value = 'class';
                };

                const editClassroom = (classroom) => {
                    isEditClassroom.value = true;
                    editingClassroomId.value = classroom.id;
                    formClassroom.name = classroom.name || '';
                    formClassroom.capacity = classroom.capacity || 50;
                    formClassroom.is_lab = !!classroom.is_lab;
                    activeModal.value = 'classroom';
                };

                const editCourse = (course) => {
                    isEditCourse.value = true;
                    editingCourseId.value = course.id;
                    formCourse.code = course.code || '';
                    formCourse.name = course.name || '';
                    formCourse.department = course.department || '';
                    formCourse.credits = course.credits || 6;
                    formCourse.course_type = course.course_type || 'Compulsory';
                    formCourse.max_block_hours = course.max_block_hours || 2;
                    formCourse.is_lab_required = !!course.is_lab_required;
                    activeModal.value = 'course';
                };

                const editRequirement = (req) => {
                    isEditReq.value = true;
                    editingReqId.value = req.id;
                    formReq.school_class = req.school_class;
                    formReq.course = req.course;
                    formReq.teacher = req.teacher;
                    formReq.weekly_hours = req.weekly_hours || 2;
                    activeModal.value = 'requirement';
                };

                const saveTeacher = async () => {
                    if (!formTeacher.name) return showToast('Please enter teacher name.', 'error');
                    const payload = { ...formTeacher };
                    if (isEditTeacher.value && editingTeacherId.value) {
                        try {
                            await axios.put(`${API_BASE}/teachers/${editingTeacherId.value}/`, payload, {
                                headers: getAuthHeaders()
                            });
                            showToast('Faculty updated successfully.', 'success');
                            closeModal();
                            loadAllData();
                        } catch (e) {
                            showToast(parseError(e), 'error');
                        }
                    } else {
                        fetchPost('teachers', payload, 'Faculty added successfully.');
                    }
                    resetTeacherForm();
                };

                const saveClass = async () => {
                    if (!formClass.name) return showToast('Cohort / Section name is required.', 'error');
                    const payload = {
                        ...formClass,
                        advisor: formClass.advisor ? formClass.advisor : null
                    };
                    if (isEditClass.value && editingClassId.value) {
                        try {
                            await axios.put(`${API_BASE}/school-classes/${editingClassId.value}/`, payload, {
                                headers: getAuthHeaders()
                            });
                            showToast('Student Cohort updated successfully.', 'success');
                            closeModal();
                            loadAllData();
                        } catch (e) {
                            showToast(parseError(e), 'error');
                        }
                    } else {
                        fetchPost('school-classes', payload, 'Student Cohort created successfully.');
                    }
                    resetClassForm();
                };

                const saveClassroom = async () => {
                    if (!formClassroom.name) return showToast('Hall / Room name is required.', 'error');
                    const payload = { ...formClassroom };
                    if (isEditClassroom.value && editingClassroomId.value) {
                        try {
                            await axios.put(`${API_BASE}/classrooms/${editingClassroomId.value}/`, payload, {
                                headers: getAuthHeaders()
                            });
                            showToast('Classroom updated successfully.', 'success');
                            closeModal();
                            loadAllData();
                        } catch (e) {
                            showToast(parseError(e), 'error');
                        }
                    } else {
                        fetchPost('classrooms', payload, 'Facility added successfully.');
                    }
                    resetClassroomForm();
                };

                const saveCourse = async () => {
                    if (!formCourse.name) return showToast('Course title is required.', 'error');
                    const payload = { ...formCourse };
                    if (isEditCourse.value && editingCourseId.value) {
                        try {
                            await axios.put(`${API_BASE}/courses/${editingCourseId.value}/`, payload, {
                                headers: getAuthHeaders()
                            });
                            showToast('Course updated successfully.', 'success');
                            closeModal();
                            loadAllData();
                        } catch (e) {
                            showToast(parseError(e), 'error');
                        }
                    } else {
                        fetchPost('courses', payload, 'Course added to catalog successfully.');
                    }
                    resetCourseForm();
                };

                const saveRequirement = async () => {
                    if (!formReq.school_class || !formReq.course || !formReq.teacher || !formReq.weekly_hours) {
                        return showToast('Please complete all assignment fields.', 'error');
                    }
                    const payload = {
                        school_class: formReq.school_class,
                        course: formReq.course,
                        teacher: formReq.teacher,
                        weekly_hours: Number(formReq.weekly_hours)
                    };
                    if (isEditReq.value && editingReqId.value) {
                        try {
                            await axios.put(`${API_BASE}/course-requirements/${editingReqId.value}/`, payload, {
                                headers: getAuthHeaders()
                            });
                            showToast('Course offering updated successfully.', 'success');
                            closeModal();
                            loadAllData();
                        } catch (e) {
                            showToast(parseError(e), 'error');
                        }
                    } else {
                        fetchPost('course-requirements', payload, 'Course assignment created successfully.');
                    }
                };

                const generateDefaultTimeSlots = async () => {
                    try {
                        const config = { headers: getAuthHeaders() };
                        for (let ts of state.timeslots) {
                            await axios.delete(`${API_BASE}/time-slots/${ts.id}/`, config);
                        }
                        for (let day of dayKeys) {
                            for (let hour = 1; hour <= 8; hour++) {
                                await axios.post(`${API_BASE}/time-slots/`, { day, hour }, config);
                            }
                        }
                        showToast('Generated 40 weekly time slots.', 'success');
                        loadAllData();
                    } catch (e) {
                        showToast('Failed to generate time slots.', 'error');
                    }
                };

                const generateSchedule = async () => {
                    showToast('Optimization engine running...', 'info');
                    try {
                        const res = await axios.post(`${API_BASE}/generate-schedule/`, {}, {
                            headers: getAuthHeaders()
                        });
                        showToast('Conflict-free schedule generated successfully!', 'success');
                        loadAllData();
                    } catch (e) {
                        const errMsg = e.response?.data?.error || 'Failed to generate schedule.';
                        showToast(errMsg, 'error');
                    }
                };

                const openModal = (modalName) => {
                    if (modalName === 'teacher') {
                        isEditTeacher.value = false;
                        editingTeacherId.value = null;
                        resetTeacherForm();
                    }
                    if (modalName === 'class') {
                        isEditClass.value = false;
                        editingClassId.value = null;
                        resetClassForm();
                    }
                    if (modalName === 'classroom') {
                        isEditClassroom.value = false;
                        editingClassroomId.value = null;
                        resetClassroomForm();
                    }
                    if (modalName === 'course') {
                        isEditCourse.value = false;
                        editingCourseId.value = null;
                        resetCourseForm();
                    }
                    if (modalName === 'requirement') {
                        isEditReq.value = false;
                        editingReqId.value = null;
                        formReq.school_class = state.classes[0]?.id || '';
                        formReq.course = state.courses[0]?.id || '';
                        formReq.teacher = state.teachers[0]?.id || '';
                        formReq.weekly_hours = 2;
                    }
                    activeModal.value = modalName;
                };

                const closeModal = () => { activeModal.value = null; };

                const getTimeSlotsForDay = (day) => {
                    return state.timeslots.filter(ts => ts.day === day).sort((a, b) => a.hour - b.hour);
                };

                const getScheduleSlot = (targetClass, day, hour) => {
                    return state.schedules.find(s => s.school_class_name === targetClass && s.day === day && s.hour === hour);
                };

                const scheduleStatsText = computed(() => {
                    if (state.schedules.length === 0) return 'No schedule generated yet';
                    return `Total ${state.schedules.length} Lesson Assignments Scheduled`;
                });

                const tabBtnClass = (tabName) => {
                    const base = 'flex-1 min-w-[140px] px-4 py-3 rounded-xl font-semibold text-sm transition-all flex items-center justify-center gap-2 ';
                    if (activeTab.value === tabName) {
                        return base + 'text-white bg-brand-600 shadow-md';
                    }
                    return base + 'text-slate-400 hover:text-white hover:bg-slate-800/50';
                };

                const printWindow = () => window.print();

                // AI Assistant State & Methods
                const showAiChat = ref(false);
                const aiInput = ref('');
                const aiLoading = ref(false);
                const aiChatContainer = ref(null);
                const aiMessages = ref([
                    {
                        role: 'assistant',
                        text: '👋 **Merhaba!** Ben ders programı optimizasyon asistanınız.\nÖğretmen müsaitlikleri, sınıf programları, çakışma analizleri veya derslik bilgileri hakkında soru sorabilirsiniz.'
                    }
                ]);

                const toggleAiChat = () => {
                    showAiChat.value = !showAiChat.value;
                    if (showAiChat.value) {
                        scrollAiChatToBottom();
                    }
                };

                const clearAiChat = () => {
                    aiMessages.value = [
                        {
                            role: 'assistant',
                            text: 'Sohbet geçmişi temizlendi. Nasıl yardımcı olabilirim?'
                        }
                    ];
                };

                const scrollAiChatToBottom = () => {
                    setTimeout(() => {
                        if (aiChatContainer.value) {
                            aiChatContainer.value.scrollTop = aiChatContainer.value.scrollHeight;
                        }
                    }, 50);
                };

                const formatAiMarkdown = (text) => {
                    if (!text) return '';
                    let formatted = text
                        .replace(/&/g, '&amp;')
                        .replace(/</g, '&lt;')
                        .replace(/>/g, '&gt;')
                        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                        .replace(/\*(.*?)\*/g, '<em>$1</em>')
                        .replace(/`([^`]+)`/g, '<code class="bg-purple-950/60 text-purple-300 px-1.5 py-0.5 rounded border border-purple-800/40 text-xs font-mono">$1</code>');
                    return formatted;
                };

                const sendAiSuggestion = (suggestionText) => {
                    aiInput.value = suggestionText;
                    sendAiMessage();
                };

                const sendAiMessage = async () => {
                    const msg = aiInput.value ? aiInput.value.trim() : '';
                    if (!msg || aiLoading.value) return;

                    aiMessages.value.push({ role: 'user', text: msg });
                    aiInput.value = '';
                    aiLoading.value = true;
                    scrollAiChatToBottom();

                    try {
                        const historyForBackend = aiMessages.value.slice(-6).map(m => ({
                            role: m.role,
                            text: m.text
                        }));

                        const res = await axios.post(`${API_BASE}/ai/chat/`, {
                            message: msg,
                            history: historyForBackend
                        }, { headers: getAuthHeaders() });

                        aiMessages.value.push({
                            role: 'assistant',
                            text: res.data.reply || 'Yanıt alınamadı.'
                        });
                    } catch (err) {
                        const errorMsg = err.response?.data?.error || err.message || 'Sunucu ile bağlantı kurulamadı.';
                        aiMessages.value.push({
                            role: 'assistant',
                            text: `⚠️ **Hata**: ${errorMsg}`
                        });
                    } finally {
                        aiLoading.value = false;
                        scrollAiChatToBottom();
                    }
                };

                onMounted(() => {
                    checkAuth();
                });

                return {
                    isLoggedIn,
                    user,
                    activeTab,
                    activeModal,
                    filterTargetClass,
                    toasts,
                    loginForm,
                    loginError,
                    state,
                    formTeacher,
                    isEditTeacher,
                    editTeacher,
                    formClass,
                    isEditClass,
                    editClass,
                    formClassroom,
                    isEditClassroom,
                    editClassroom,
                    formCourse,
                    isEditCourse,
                    editCourse,
                    formReq,
                    isEditReq,
                    editRequirement,
                    deleteModalConfig,
                    confirmDelete,
                    executeConfirmedDelete,
                    dayKeys,
                    handleLogin,
                    handleLogout,
                    openModal,
                    closeModal,
                    saveTeacher,
                    saveClass,
                    saveClassroom,
                    saveCourse,
                    saveRequirement,
                    showDeleteModal,
                    deleteTarget,
                    handleConfirmDelete,
                    confirmDelete,
                    generateDefaultTimeSlots,
                    generateSchedule,
                    getTimeSlotsForDay,
                    getScheduleSlot,
                    scheduleStatsText,
                    tabBtnClass,
                    printWindow,
                    currentLang,
                    setLanguage,
                    t,
                    // AI Assistant exports
                    showAiChat,
                    aiInput,
                    aiLoading,
                    aiMessages,
                    aiChatContainer,
                    toggleAiChat,
                    clearAiChat,
                    sendAiMessage,
                    sendAiSuggestion,
                    formatAiMarkdown
                };


            }
        });
        app.mount('#app');
    