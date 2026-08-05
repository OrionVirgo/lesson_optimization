# 📅 Lesson Scheduling & Optimization System (OptiSchedule AI)

Okul ve derslik bazlı ders programı oluşturmayı otomatikleştiren, çakışmasız (conflict-free) ders dağıtımı yapan modern **Vue 3 + Vite + TypeScript** ve **Django REST Framework** tabanlı web uygulaması.

---

## 🚀 Özellikler

- **🤖 Otomatik Optimizasyon Motoru**: Öğretmen müsaitliği, sınıf kontenjanları, derslik kapasitesi ve laboratuvar gereksinimlerine göre çakışmasız ders programı üretir (`scheduler.py`).
- **✨ Gemini AI Asistanı**: Doğal dilde soru sorma, boş derslik sorgulama, öğretmen yükü özeti ve çakışma analiz raporlama altyapısı (`ai_assistant.py`).
- **🌐 Çoklu Dil Desteği (i18n)**: Türkçe ve İngilizce dil seçenekleri.
- **🎨 Vue 3 & Vite & TypeScript**: Modern, reaktif, cam efekti (glassmorphic) koyu tema ve duyarlı (responsive) ön yüz.
- **🔐 JWT Tabanlı Kimlik Doğrulama**: Güvenli oturum açma, jeton yenileme ve rol tabanlı koruma.
- **🖨️ Yazdırma Desteği**: Haftalık ders programlarını çıktıya hazır formatta görüntüleme ve yazdırma.

---

## 🛠️ Teknolojiler

- **Backend**: Python 3.10+, Django 5, Django REST Framework, SimpleJWT, Google Gemini GenAI SDK, SQLite / PostgreSQL
- **Frontend**: Vue 3 (Composition API), Vite, TypeScript, vue-i18n, Axios, Lucide Icons

---

## 📁 Proje Yapısı

```
lesson_optimization/
├── backend/
│   ├── api/                  # Django REST API uygulaması (Modeller, Viewset'ler, Optimizasyon Motoru & AI)
│   ├── config/               # Django proje ayarları ve URL yapılandırması
│   └── manage.py
├── frontend/
│   ├── src/                  # Vue 3 + TypeScript kaynak kodları (views, components, i18n, services)
│   ├── package.json
│   └── vite.config.ts
├── package.json              # Ana proje scriptleri (Concurrent dev server)
├── requirements.txt          # Python bağımlılıkları
└── README.md
```

---

## 💻 Kurulum ve Tek Komutla Çalıştırma

### 1. Bağımlılıkları Yükleyin

```bash
# Backend bağımlılıkları
pip install -r requirements.txt

# Frontend & Root bağımlılıkları
npm install
cd frontend && npm install && cd ..
```

### 2. Tek Komutla Başlatın (Backend + Frontend)

Proje kök dizininde aşağıdaki komutu çalıştırmanız yeterlidir:

```bash
npm start
```
veya
```bash
npm run dev
```

* **Frontend Arayüzü:** `http://localhost:5173`
* **Backend REST API:** `http://127.0.0.1:8000/api/`

---

## 📄 Lisans
Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
