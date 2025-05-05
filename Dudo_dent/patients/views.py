from django.shortcuts import render

# Create your views here.

def all_patients(request):
    return render(request, 'patients/patients-main.html')