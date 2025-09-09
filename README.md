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



