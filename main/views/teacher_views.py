from datetime import date
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def teachers(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')
    
    data={
        'page' : 'teachers'
    }
    
    return render(request, "./main/teacher/teachers.html", data)
 
def add(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')
    
    data={
        'page' : 'teachers'
    }
    
    return render(request, "./main/teacher/add-teacher.html", data)


