# Football Shop — Tugas 2 PBP

Nama: Febrian Abimanyu Wijanarko
NPM: 2406397984
Kelas: PBP D

Live: http://febrian-abimanyu-footballshop.pbp.cs.ui.ac.id
Repo: https://github.com/bimanyuw/football-shop


A. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

    1. Inisiasi repo & environment
    -> git init, buat .venv, install django, gunicorn, whitenoise, generate requirements.txt.

    2. Buat project & app
    -> django-admin startproject footballshop .
    -> python manage.py startapp main
    -> Tambahkan 'main' ke INSTALLED_APPS.

    3. Routing
    -> footballshop/urls.py → path('', include('main.urls')),
    -> main/urls.py → mapping '' ke view utama.

    4. View + Template identitas
    -> main/views.py merender main/index.html berisi nama aplikasi, nama, dan kelas.

    5. Model
    -> main/models.py menambahkan Product dengan 6 field wajib (+opsional).
    -> python manage.py makemigrations && python manage.py migrate.

    6. Static & Deploy prep
    -> Tambah whitenoise di MIDDLEWARE.
    -> Buat Procfile: web: bash -c "python manage.py migrate --noinput && gunicorn footballshop.wsgi"
    -> Buat runtime.txt: python-3.11.9.

    7. Deploy ke PWS
    -> Buat project PWS, tambahkan remote pws, tambahkan domain PWS ke ALLOWED_HOSTS.
    -> git push pws master, tunggu Building → Running.

    8. Admin
    -> python manage.py createsuperuser untuk lokal.
    -> Di PWS, login /admin (superuser bisa dibuat manual via Environs + script atau langsung input data setelah login).

B. Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.
    
    Gambar Bagan MVT Django – Football Shop :
        https://drive.google.com/file/d/1dUeF1AXKoWNUNnuIDooFi0Elj_Qhs7xl/view?usp=sharing

    Penjelasan :
        Ketika browser membuka URL aplikasi, request pertama kali pergi ke project/urls.py. File ini bekerja sebagai gerbang utama yang memeriksa URL masuk. Untuk path root (/), request diteruskan ke main/urls.py. Pada main/urls.py, URL itu dipetakan ke fungsi di views.py (misalnya home() atau show_main()).

        Di views.py, logika jalan. Ketika butuh data, view akan meminta data ke model lewat ORM—contohnya Product.objects.all(). ORM ini yang bekerja sama dengan database dan mengembalikan hasilnya ke view dalam bentuk QuerySet/objek. Setelah mendapat data, view akan membuat context lalu render template (main.html) menggunakan render(request, template, context). Hasilnya menjadi HTML dan dikirim kembali ke browser sebagai respons HTTP 200. Ketika URL-nya tidak ditemukan di urls.py, server akan mengembalikan 404.

C. Jelaskan peran settings.py dalam proyek Django!

  settings.py adalah pusat konfigurasi proyek. Di berkas ini saya menentukan aplikasi yang aktif (INSTALLED_APPS), middleware (termasuk WhiteNoise untuk static files), konfigurasi template, database (development SQLite; production dapat diarahkan ke PostgreSQL melalui environment variables), pengelolaan static files (STATIC_ROOT, STATICFILES_STORAGE), serta aspek keamanan seperti SECRET_KEY, DEBUG, dan ALLOWED_HOSTS. Singkatnya, settings.py memastikan satu sumber kebenaran untuk perilaku aplikasi di lingkungan development maupun production.

D. Bagaimana cara kerja migrasi database di Django?

  Saat model berubah, perintah python manage.py makemigrations menghasilkan berkas migrasi yang berisi instruksi perubahan skema (misalnya membuat tabel main_product atau menambah kolom). Perintah python manage.py migrate mengeksekusi instruksi tersebut terhadap database dan mencatatnya pada tabel django_migrations sehingga Django tahu migrasi mana yang sudah diterapkan. Mekanisme ini membuat skema database selalu versi-terkendali, aman untuk di-deploy, serta tidak perlu menulis SQL mentah.

E. Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?

  Django “batteries-included”: ORM, templating, autentikasi, admin, session, dan middleware tersedia sejak awal. Pola MVT memisahkan tampilan, logika, dan data dengan jelas sehingga mahasiswa cepat memahami arsitektur web modern. Dokumentasinya komprehensif, komunitasnya besar, dan praktik keamanannya baik secara default. Kombinasi tersebut membuat kurva belajar mulus namun tetap realistis untuk membangun aplikasi beneran dan di-deploy.

F. Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?

  Tidak ada

