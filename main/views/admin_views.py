from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from main.models import Logs
# Create your views here.
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    # if not request.user.is_superuser:
    #     return redirect('/')
    recent_logs = Logs.objects.filter(search_field = str(datetime.now().strftime('%B %d, %Y - %A'))).order_by('-date')[:10]   
    data={
        'page' : 'dashboard',
        'recent_logs': recent_logs  
    }
    print(datetime.now())
    
    return render(request, "./main/admin/dashboard.html", data)

