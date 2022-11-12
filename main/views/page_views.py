from datetime import date
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from main.models import MyUser

# admin = MyUser()
# admin.is_superuser = 1
# admin.id_no = 'LIB-123'
# admin.set_password('admin')
# admin.save()

# Create your views here.
def landing(request):    
    return redirect('/login')

def login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    
    message = ''
    id_no = ''
    password = ''

    if request.method == 'POST':
        id_no = request.POST['id_no']
        password = request.POST['password']

        user = authenticate(id_no=id_no, password=password)
        if user is not None:
            auth_login(request, user)

            if user.is_superuser:
                return redirect("/dashboard")
        
        else:
            message = "Invalid username and/or password."

    return render(request, 'login.html', {'message': message, 'id_no': id_no, 'password': password})

def logout(request):
    auth_logout(request)
    return redirect('/login')

