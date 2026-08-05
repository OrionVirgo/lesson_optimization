export default {
  app: {
    title: 'Ders Programı Optimizasyon Portalı',
    subtitle: 'Çakışmasız Ders Programı Oluşturucu ve Gemini AI Asistanı'
  },
  nav: {
    dashboard: 'Ders Programı',
    teachers: 'Öğretmenler',
    classes: 'Sınıflar',
    classrooms: 'Derslikler',
    courses: 'Dersler',
    timeslots: 'Zaman Dilimleri',
    requirements: 'Ders Atamaları',
    aiAssistant: 'AI Asistan'
  },
  actions: {
    add: 'Yeni Ekle',
    edit: 'Düzenle',
    delete: 'Sil',
    save: 'Kaydet',
    cancel: 'İptal',
    close: 'Kapat',
    generateSchedule: 'Programı Otomatik Oluştur',
    generating: 'Optimizasyon Hesaplanıyor...',
    print: 'Programı Yazdır / PDF',
    filter: 'Filtrele',
    all: 'Tümü',
    search: 'Ara...',
    confirm: 'Onayla'
  },
  timetable: {
    title: 'Haftalık Ders Programı Matrisi',
    selectClass: 'Sınıf Seçin:',
    selectTeacher: 'Öğretmen Seçin:',
    allClasses: 'Tüm Sınıflar',
    allTeachers: 'Tüm Öğretmenler',
    emptySlot: 'Boş Ders Saati',
    conflictWarning: 'Olası Çakışma Tespit Edildi!',
    labRequired: 'Lab Zorunlu',
    offDay: 'İzin Günü',
    generatedSuccess: 'Ders programı başarıyla çakışmasız olarak oluşturuldu!',
    generatedError: 'Kısıtlar nedeniyle çakışmasız ders programı oluşturulamadı.'
  },
  teachers: {
    title: 'Öğretmen Yönetimi',
    name: 'Ad Soyad',
    titleBranch: 'Unvan / Branş',
    offDay: 'İzin Günü',
    phone: 'Telefon',
    email: 'E-Posta',
    maxHours: 'Maks. Günlük Ders',
    actions: 'İşlemler'
  },
  classes: {
    title: 'Sınıf Yönetimi',
    name: 'Sınıf Adı',
    gradeLevel: 'Sınıf Seviyesi',
    studentCount: 'Öğrenci Sayısı'
  },
  classrooms: {
    title: 'Derslik / Laboratuvar Yönetimi',
    name: 'Derslik Adı',
    building: 'Bina / Blok',
    capacity: 'Kapasite',
    isLab: 'Laboratuvar mı?'
  },
  courses: {
    title: 'Ders Kataloğu',
    code: 'Ders Kodu',
    name: 'Ders Adı',
    isLabRequired: 'Lab Zorunluluğu Var mı?'
  },
  timeslots: {
    title: 'Zaman Dilimleri',
    day: 'Gün',
    hour: 'Saat / Ders Numarası',
    timeRange: 'Saat Aralığı'
  },
  requirements: {
    title: 'Ders Atamaları ve Kısıtlar',
    schoolClass: 'Hedef Sınıf',
    course: 'Atanacak Ders',
    teacher: 'Görevli Öğretmen',
    weeklyHours: 'Haftalık Ders Saati'
  },
  ai: {
    title: 'Gemini AI Asistanı',
    placeholder: 'Ders programı, öğretmen izinleri veya çakışmalar hakkında soru sorun...',
    quickQuestions: 'Hızlı Sorular:',
    q1: 'Ders programında çakışma var mı?',
    q2: 'Boş derslikleri listele',
    q3: 'Öğretmen yüklerini özetle',
    sending: 'Yanıtlanıyor...'
  }
}
