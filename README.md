# Football Shop — Tugas 2 PBP

Nama: Febrian Abimanyu Wijanarko
NPM: 2406397984
Kelas: PBP D

Live: http://febrian-abimanyu-footballshop.pbp.cs.ui.ac.id
Repo: https://github.com/bimanyuw/football-shop


**TUGAS 2**
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

**TUGAS 3**
A. Mengapa perlu data delivery di platform?

  Aplikasi modern sering punya lebih dari satu klien seperti web, mobile, dan service lainnya. Data delivery adalah endpoint yang mengirim data mentah seperti JSON/XML yang memisahkan data dari presentasi, sehingga klien berbeda bisa memakai sumber data yang sama, integrasi ke sistem lain seperti ETL, analytics, dan mikroservis lebih mudah caching & versioning API bisa dikelola terpisah dari UI, dan pengujian jadi jelas karena kontrak datanya eksplisit.

B. XML vs JSON—mana lebih baik? Mengapa JSON lebih populer? 

  Keduanya sama-sama bisa merepresentasikan data terstruktur. Namun, JSON lebih populer karena sintaks nya ringkas & dekat dengan struktur objek di JavaScript/Python, parsing lebih cepat & payload lebih kecil untuk kebanyakan kasus, dan lebih enak dibaca dan ditulis secara manual. Di sisi lain, XML masih relevan untuk skenario dokumen berat, tapi untuk web API umum, JSON biasanya lebih efisien.

C. Fungsi `is_valid()` pada form Django dan kenapa dibutuhkan? 

  `is_valid()` menjalankan validasi untuk memeriksa tipe data, field wajib, batas nilai, serta validasi kustom `clean_*`. Jika valid, `form.cleaned_data` terisi aman digunakan/ disimpan. Tanpa validasi ini, data yang masuk bisa salah/berbahaya.

D. Mengapa butuh `csrf_token` pada form Django? Apa risikonya kalau tidak ada? Bagaimana penyerang memanfaatkannya?

  `csrf_token` mencegah Cross-Site Request Forgery yaitu dimana penyerang menipu browser korban agar mengirim POST ke situs tanpa sepengetahuan korban. Token unik per sesi memastikan hanya form sah dari situs yang diterima. Tanpa token, attacker bisa meletakkan form tersembunyi di situs lain yang menembak endpoint dengan kredensial korban.

E. Cara implementasi checklist (step-by-step)

  - Membuat `ProductForm` (ModelForm) → `forms.py`.  
  - Menambah view `create_product()` untuk handle GET/POST, panggil `is_valid()`, `save()`, redirect ke `show_main`.  
  - Membuat `product_detail()` untuk menampilkan detail item.  
  - Membuat 4 endpoint data delivery: `show_xml`, `show_json`, `show_xml_by_id`, `show_json_by_id` dengan `django.core.serializers`.  
  - Routing semua path di `main/urls.py` (termasuk memperbaiki `show_main`).  
  - Update `index.html` → tombol Add** (ke `/add`) & Detail (per item).  
  - Buat `create_product.html` dan `product_detail.html`.  
  - Cek di browser & Postman (GET ke `/xml/`, `/json/`, `/xml/<id>/`, `/json/<id>/`).  
  - Commit & push.

F. Feedback untuk asdos (Tutorial 2)
  Tidak ada

G. Bukti akses 4 URL dengan Postman
  https://docs.google.com/document/d/1Vdt5iS2ThLA-VVtDcaSFVPgYhtiEnV1wWC5raiPi6gE/edit?tab=t.0

*TUGAS 4*
A. Apa itu Django AuthenticationForm?
  AuthenticationForm adalah form bawaan Django yang digunakan untuk proses login pengguna.
  Kelebihan:
  - Tidak perlu membuat form manual untuk login (sudah ada field username & password).
  - Terintegrasi langsung dengan sistem autentikasi Django.
  - Menyediakan validasi otomatis (contoh: username/password salah).
  Kekurangan:
  - Kurang fleksibel kalau mau menambahkan field custom (misalnya login dengan email).
  - Tampilan default sederhana, biasanya perlu dikustomisasi.

B. Apa perbedaan autentikasi dan otorisasi? Bagaimana Django mengimplementasikan keduanya?
  Autentikasi adalah proses verifikasi identitas user (contoh: login dengan username & password), sementara otorisasi adalah proses pemberian izin akses setelah autentikasi berhasil (contoh: hanya admin boleh akses halaman admin).

  Implementasi di Django:
  - Autentikasi: memakai User model, AuthenticationForm, authenticate(), dan login().
  - Otorisasi: memakai @login_required decorator, permissions, dan is_staff/is_superuser untuk    membatasi akses.


C. Apa saja kelebihan dan kekurangan session dan cookies dalam konteks menyimpan state di aplikasi web?
  Session
  - Kelebihan: Data disimpan di server, lebih aman, bisa menyimpan data besar.
  - Kekurangan: Membutuhkan resource server lebih banyak.

  ookies
  - Kelebihan: Disimpan di client/browser, tidak membebani server, sederhana untuk data kecil (misalnya last_login).
  - Kekurangan: Mudah diutak-atik oleh user, ukuran terbatas (±4KB), ada risiko keamanan (XSS/CSRF).

D. Apakah penggunaan cookies aman secara default dalam pengembangan web?
  Cookies tidak sepenuhnya aman secara default, karena bisa disadap/diubah jika tidak dikonfigurasi dengan benar. Adapaun risikonya seperti XSS, CSRF, dan juga pencurian cookie (session hijacking).Django dapat menangani risiko-risiko tersebut dengan:
  - HttpOnly cookies → tidak bisa diakses via JavaScript.
  - CSRF token → mencegah CSRF attack.
  - SESSION_COOKIE_SECURE = True (hanya lewat HTTPS)

E. Step-by-Step Implementasi Checklist
  1. Mengimplementasikan fungsi registrasi, login, logout
  Pertama, saya mengimplementasikan fungsi registrasi, login, dan logout. Hal ini dilakukan dengan menambahkan tiga fungsi utama, yaitu register, login_user, dan logout_user pada views.py. Untuk mendukung fungsi tersebut, saya juga membuat dua berkas template baru, yaitu register.html dan login.html sebagai form autentikasi. Selanjutnya, saya menambahkan path pada urls.py agar halaman /register/, /login/, dan /logout/ dapat diakses oleh pengguna.

  2. Menghubungkan model Product dengan User
  Kedua, saya menghubungkan model Product dengan User. Caranya adalah dengan menambahkan field 

  *user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)*
  
  pada models.py. Dengan adanya field ini, setiap produk yang dibuat akan otomatis terikat pada user yang membuatnya, sehingga data produk dapat dipersonalisasi sesuai akun pengguna.

  3. Menampilkan detail user login dan cookie last_login
  Ketiga, saya menambahkan fitur untuk menampilkan detail user login dan cookie last_login. Pada fungsi login_user, saya menambahkan baris kode 

  *response.set_cookie('last_login', str(datetime.datetime.now()))*
  
  untuk menyimpan informasi waktu login terakhir. Sementara itu, pada fungsi logout_user saya menambahkan 
  
  *response.delete_cookie('last_login')*
  
  agar cookie tersebut terhapus ketika pengguna logout. Informasi waktu login terakhir ini kemudian ditampilkan di halaman utama index.html dengan menambahkan kode {{ last_login }}.

  4. Membatasi akses halaman
  Terakhir, saya melakukan pembatasan akses halaman dengan menggunakan decorator 
  
  *@login_required(login_url='/login/')*
  
  Sebagai contoh, decorator ini saya terapkan pada fungsi show_main agar hanya pengguna yang sudah login yang dapat mengakses halaman utama aplikasi. Dengan cara ini, sistem dapat lebih aman dan sesuai dengan status autentikasi pengguna.

  *Tugas 5*
  A. Prioritas CSS selector: urutannya adalah inline style paling tinggi, kemudian selector ID, lalu class/atribut/pseudo-class, lalu tag/element selector. Jika ada selector dengan tingkat spesifik yang sama, maka yang ditulis paling akhir di file CSS akan dipakai.

  B. Responsive design penting supaya tampilan web tetap nyaman digunakan di berbagai ukuran layar (HP, tablet, laptop, desktop). Tanpa responsive design tampilan bisa berantakan di HP, sedangkan dengan responsive design semua elemen menyesuaikan ukuran layar. Contohnya, Tokopedia atau Shopee sudah responsif sehingga nyaman diakses dari ponsel maupun PC, sedangkan situs lama yang hanya untuk desktop tidak responsif dan teks/tombol jadi terlalu kecil di HP.

  C. Margin, border, padding: margin adalah jarak luar elemen dengan elemen lain, border adalah garis tepi yang membungkus elemen, padding adalah jarak dalam antara isi konten dengan border.

  D. Flexbox dan grid: Flexbox dipakai untuk layout satu dimensi (baris atau kolom), cocok untuk navbar atau align item secara horizontal/vertical. Grid dipakai untuk layout dua dimensi (baris dan kolom), cocok untuk menata galeri atau card layout yang rapi.

  E. Langkah implementasi:
  - Menambahkan fitur edit dan delete product di views, lalu menampilkan tombol edit dan hapus di setiap card produk.

  - Mengubah desain halaman login, register, tambah/edit produk, daftar produk, dan detail produk agar sesuai color palette (hitam, maroon, beige, cream).

  - Membuat navbar responsif yang berubah menjadi hamburger menu di mobile.

  - Mendesain card produk dengan hover effect, harga diformat ribuan, dan aksi edit/hapus untuk owner.

  - Mendesain halaman detail produk dengan layout dua kolom (gambar besar di kiri, detail di kanan), menampilkan harga rapih, deskripsi, dan rating bintang.