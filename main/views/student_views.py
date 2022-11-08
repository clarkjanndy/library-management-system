from datetime import date
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from main.models import MyUser

# admin = MyUser()
# admin.is_superuser = 1
# admin.id_no = 'LIB-123'
# admin.set_password('admin')
# admin.save()

# Create your views here.
def students(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')
    
    data={
        'page' : 'students'
    }
    
    return render(request, "./main/student/students.html", data)

def add(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')
    
    data={
        'page' : 'students'
    }
    
    return render(request, "./main/student/add-student.html", data)

