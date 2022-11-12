from datetime import date
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect


# Create your views here.
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    # if not request.user.is_superuser:
    #     return redirect('/')
    
    data={
        'page' : 'dashboard'
    }
    
    return render(request, "./main/admin/dashboard.html", data)

