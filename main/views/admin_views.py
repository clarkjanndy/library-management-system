from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from main.models import Logs
# Create your views here.
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/books')
    
    recent_logs = Logs.objects.filter(search_field = str(datetime.now().strftime('%B %d, %Y - %A'))).order_by('-date')[:10]   
    data={
        'page' : 'dashboard',
        'recent_logs': recent_logs  
    }
    print(datetime.now())
    
    return render(request, "./main/admin/dashboard.html", data)

def my_profile(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.user.is_staff:
        return redirect('/teachers/{id_no}'.format(id_no=request.user.id_no))

    return redirect('/students/{id_no}'.format(id_no=request.user.id_no))  
