# 📅 Lesson Scheduling & Optimization System

Okul ve derslik bazlı ders programı oluşturmayı otomatikleştiren, çakışmasız (conflict-free) ders dağıtımı yapan modern bir web uygulaması.

---

## 🚀 Özellikler

- **🤖 Otomatik Optimizasyon Motoru**: Öğretmen müsaitliği, sınıf kontenjanları, derslik kapasitesi ve laboratuvar gereksinimlerine göre çakışmasız ders programı üretir.
- **🔐 JWT Tabanlı Kimlik Doğrulama**: Güvenli oturum açma, jeton yenileme ve rol tabanlı koruma.
- **🎨 Vue 3 & Tailwind CSS**: Kullanıcı dostu, modern, koyu tema destekli ve duyarlı (responsive) ön yüz.
- **⚡ Axios Entegrasyonu**: Asenkron ve güvenli API veri iletişimi.
- **📊 Yönetim Paneli**: Öğretmenler, Sınıflar, Derslikler, Dersler ve Ders Gereksinimlerinin yönetimi.
- **🖨️ Yazdırma Desteği**: Haftalık ders programlarını çıktıya hazır formatta görüntüleme ve yazdırma.

---

## 🛠️ Teknolojiler

- **Backend**: Python 3.10+, Django 5, Django REST Framework, SimpleJWT, SQLite / PostgreSQL
- **Frontend**: Vue 3 (Composition API), Axios, Tailwind CSS, FontAwesome

---

## 📁 Proje Yapısı

```
lesson_optimization/
├── backend/
│   ├── api/                  # Django REST API uygulaması (Modeller, Viewset'ler, Optimizasyon Motoru)
│   ├── config/               # Django proje ayarları ve URL yapılandırması
│   └── manage.py
├── frontend/
│   └── templates/            # Vue 3 SPA şablonları, bileşenleri (interface.html, DeleteModal vb.)
├── .env.example              # Ortam değişkenleri şablonu
├── .gitignore                # Git tarafından yoksayılacak dosyalar
├── requirements.txt          # Python bağımlılıkları
└── README.md
```

---

## 💻 Kurulum ve Çalıştırma

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/kullanici-adi/lesson_optimization.git
cd lesson_optimization
```

### 2. Sanal Ortam Oluşturun ve Aktif Edin
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Ayarlayın
`.env.example` dosyasını kopyalayarak `.env` dosyası oluşturun:
```bash
# Windows (PowerShell)
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

### 5. Veritabanı Göçlerini Uygulayın
```bash
cd backend
python manage.py migrate
```

### 6. Süper Kullanıcı (Admin) Oluşturun
```bash
python manage.py createsuperuser
```

### 7. Sunucuyu Başlatın
```bash
python manage.py runserver
```

Uygulama varsayılan olarak `http://127.0.0.1:8000/` adresinde çalışacaktır.

---

## 📡 API Uç Noktaları (Endpoints)

| Yöntem | Uç Nokta | Açıklama |
|---|---|---|
| `POST` | `/api/auth/login/` | Kullanıcı girişi ve JWT jeton alma |
| `GET` | `/api/auth/me/` | Oturum açan kullanıcı bilgisi |
| `GET / POST` | `/api/teachers/` | Öğretmen listeleme ve ekleme |
| `GET / POST` | `/api/school-classes/` | Sınıf listeleme ve ekleme |
| `GET / POST` | `/api/classrooms/` | Derslik listeleme ve ekleme |
| `GET / POST` | `/api/courses/` | Ders listeleme ve ekleme |
| `GET / POST` | `/api/course-requirements/` | Ders atama gereksinimleri |
| `POST` | `/api/generate-schedule/` | Optimizasyon motorunu tetikleme |

---

## 📄 Lisans
Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
