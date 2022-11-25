from datetime import date
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from main.utils.upload_photo import rename_and_upload

from main.models import MyUser, Teacher, BorrowedBook
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

def profile(request, id_no):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser and not request.user.id_no == id_no:
        return redirect('/')

    teacher = Teacher.objects.get(user__id_no=id_no)
    borrowed = BorrowedBook.objects.filter(user = teacher.user, status="borrowed")
    
    print(borrowed)

    data = {    
        'page': 'teachers',
        'teacher': teacher,
        'borrowed': borrowed
    }

    return render(request, "./main/teacher/profile.html", data)

 
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
        messages.success(request, 'Teacher added successfully')
        return redirect('/teachers/{id}'.format(id=user.id_no))
    
    data={
        'page' : 'teachers'
    }
    
    return render(request, "./main/teacher/add-teacher.html", data)


def edit(request, id_no):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser and not request.user.id_no == id_no:
        return redirect('/')

    teacher = Teacher.objects.get(user__id_no=id_no)
    if request.method == 'POST':
        teacher.user.first_name = request.POST['first_name']
        teacher.user.middle_name = request.POST['middle_name']
        teacher.user.last_name = request.POST['last_name']
        teacher.user.ext_name = request.POST['ext_name']
        teacher.user.gender = request.POST['gender']
        teacher.user.civil_status = request.POST['civil_status']
        teacher.user.address = request.POST['address']
        teacher.user.contact_no = request.POST['contact_no']
        teacher.user.is_superuser = request.POST['role']
        teacher.designation = request.POST['designation']
        teacher.year_of_exp = request.POST['year_of_exp']
        teacher.advisory = request.POST['advisory']

        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            teacher.user.photo = rename_and_upload(photo, teacher.user.id_no)

        teacher.user.save()
        teacher.save()

        messages.success(request, 'Profile updated successfully')
    return redirect('/teachers/{id}'.format(id=teacher.user.id_no))
