from django.shortcuts import render, redirect

# Create your views here.

def landing(request):
    if request.user.is_authenticated:
        pass
    
    return redirect('/login')

def login(request):
    if request.user.is_authenticated:
        pass
    
    return render(request, 'login.html')

