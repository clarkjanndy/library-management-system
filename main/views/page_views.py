from datetime import date
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from main.models import MyUser, Teacher, BookCategory

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from main.utils.upload_photo import rename_and_upload


# Create your views here.
def initialize(request):
    if MyUser.objects.all().exists():
        return HttpResponse(status=403)
    
    admin = MyUser()
    admin.is_superuser = 1
    admin.is_staff = 1
    admin.id_no = 'ADM-123'
    admin.set_password('admin')
    admin.save()

    teacher = Teacher(designation='Librarian', year_of_exp=0,
                    advisory="None", user=admin)
    teacher.save()

    BookCategory.objects.bulk_create([
        BookCategory(name='Filipiniana', limit=72, rate=0.84),
        BookCategory(name='Reserve Circulation', limit=17, rate=15),
        BookCategory(name='Fiction Books', limit=72, rate=0.63),
        BookCategory(name='Thesis', limit=72, rate=0.63),
        BookCategory(name='General Reference', limit=72, rate=0.63)
    ])
    
    messages.success(request, 'Database set-up successful.') 
    return redirect('/login')

def landing(request):
    return redirect('/login')


def login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')

    message = ''
    id_no = ''
    password = ''
    agree=''

    if request.method == 'POST':
        id_no = request.POST['id_no']
        password = request.POST['password']
        agree = request.POST['agree']

        user = authenticate(id_no=id_no, password=password)
        if user is not None:
            auth_login(request, user)

            if user.is_superuser:
                return redirect("/dashboard")
            else:
                return redirect("/books")

        else:
            messages.error(request, "Invalid Credentials.")
    print(agree)
    return render(request, 'login.html', {'id_no': id_no, 'password': password, 'agree': agree})


def change_password(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        me = MyUser.objects.get(id_no=request.user.id_no)
        me.set_password(request.POST['newpassword'])
        me.save()

        messages.success(request, "Password successfully changed.")
        return redirect('/')
    data = {'page': 'change-password', }
    return render(request, "change-password.html", data)
import base64
class UpdatePhoto(GenericAPIView):

    def post(self, request):
        
        decoded_data=base64.b64decode((request.data['photoStore']))
        rename_and_upload(request.data['photoStore'],'STUD-123')
        
        messages.success(request, 'Photo uploaded successfully.')
        return Response('success')

def logout(request):
    auth_logout(request)
    return redirect('/login')
