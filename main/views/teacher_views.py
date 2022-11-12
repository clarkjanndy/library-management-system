from datetime import date
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from main.models import MyUser, Teacher
# Create your views here.
def teachers(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')
    
    teachers = Teacher.objects.select_related('user')
    
    data={
        'page' : 'teachers',
        'teachers':teachers
    }
    
    return render(request, "./main/teacher/teachers.html", data)
 
def add(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')

    if request.method == 'POST':
        #create user instance
        user = MyUser(
            id_no = request.POST['id_no'],
            password = 'P@ssw0rd',
            first_name = request.POST['first_name'],
            middle_name = request.POST['middle_name'],
            last_name = request.POST['last_name'],
            ext_name = request.POST['ext_name'],
            gender = request.POST['gender'],
            civil_status = request.POST['civil_status'],
            address = request.POST['address'],
            contact_no = request.POST['contact_no'],
            is_staff = 1
        )
        user.set_password('P@ssw0rd')
        #save user instance
        user.save()
        
        #create teacher instance
        teacher = Teacher(
            user = user,
            designation = request.POST['designation'],
            year_of_exp = request.POST['year_of_exp'],
            advisory = request.POST['advisory'],
        )
        #save teacher instance
        teacher.save()
    
    data={
        'page' : 'teachers'
    }
    
    return render(request, "./main/teacher/add-teacher.html", data)


