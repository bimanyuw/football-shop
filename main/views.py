from django.shortcuts import render

def home(request):
    return render(request, 'main/index.html', {
        'app_name': 'Football Shop',
        'student_name': 'Febrian Abimanyu Wijanarko',
        'student_class': 'PBP CSGE602022 – 2025/2026',
    })
