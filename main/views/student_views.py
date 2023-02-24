from datetime import date
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect


from main.models import MyUser, Student, BorrowedBook
from main.utils.upload_photo import rename_and_upload

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from main.utils.upload_photo import rename_and_upload
import base64

# Create your views here.


def students(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/')

    students = Student.objects.select_related('user')

    data = {
        'page': 'students',
        'students': students
    }

    return render(request, "./main/student/students.html", data)

def profile(request, id_no):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser and not request.user.id_no == id_no:
        return redirect('/')

    student = Student.objects.get(user__id_no=id_no)
    borrowed = BorrowedBook.objects.filter(user= student.user, status="borrowed")

    data = {
        'page': 'students',
        'student': student,
        'borrowed': borrowed
    }

    return render(request, "./main/student/profile.html", data)


def add(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/')

    if request.method == 'POST':
        # create user instance
        user = MyUser(
            id_no=request.POST['id_no'],
            first_name=request.POST['first_name'],
            middle_name=request.POST['middle_name'],
            last_name=request.POST['last_name'],
            ext_name=request.POST['ext_name'],
            gender=request.POST['gender'],
            civil_status=request.POST['civil_status'],
            address=request.POST['address'],
            contact_no=request.POST['contact_no']
        )
        user.set_password('password')
        # save user instance
        user.save()

        # create student instance
        student = Student(
            user=user,
            course=request.POST['course'],
            year=request.POST['year'],
            section=request.POST['section'],
        )
        # save student instance
        student.save()
        
        messages.success(request, 'Student added successfully')
        return redirect('/students/{id}'.format(id=user.id_no))

    data = {
        'page': 'students'
    }

    return render(request, "./main/student/add-student.html", data)

def edit(request, id_no):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser and not request.user.id_no == id_no:
        return redirect('/')

    student = Student.objects.get(user__id_no=id_no)
    if request.method == 'POST':
        student.user.first_name = request.POST['first_name']
        student.user.middle_name = request.POST['middle_name']
        student.user.last_name = request.POST['last_name']
        student.user.ext_name = request.POST['ext_name']
        student.user.gender = request.POST['gender']
        student.user.civil_status = request.POST['civil_status']
        student.user.address = request.POST['address']
        student.user.contact_no = request.POST['contact_no']
        student.course = request.POST['course']
        student.year = request.POST['year']
        student.section = request.POST['section']

        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            student.user.photo = rename_and_upload(photo, student.user.id_no)
            
            print(type(request.FILES['photo']))

        student.user.save()
        student.save()

        messages.success(request, 'Profile updated successfully')
    return redirect('/students/{id}'.format(id=student.user.id_no))

class UpdatePhoto(GenericAPIView):

    def post(self, request, id_no):
        photo = rename_and_upload(request.data['photoStore'], id_no)
        
        student=MyUser.objects.get(id_no=id_no)
        student.photo = photo
        student.save()
        
        messages.success(request, 'Photo uploaded successfully.')
        return Response('success')
