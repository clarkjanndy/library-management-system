from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from main.models import MyUser, Log, Book, Activity

from django.db.models.functions import TruncDay, TruncMonth
from django.db.models import Count
# Create your views here.


def log_window(request):
    if not request.user.is_authenticated:
        return redirect('/')

    # if not request.user.is_superuser:
    #     return redirect('/')
    data = {}
    if request.method == 'POST':
        user = MyUser.objects.get(id_no=request.POST['id_no'])
        last_log = Log.objects.filter(user=user).last()

        action = 'has login'
        if last_log is not None:
            if last_log.action == 'has login':
                action = 'has logout'
            else:
                action = 'has login'

        log = Log(
            user=user,
            date=datetime.now(),
            action=action,
            search_field=str(datetime.now().strftime('%B %d, %Y - %A'))
        )
        log.save()
        
        Activity.objects.create(user=log.user, action = log.action)

        data['user'] = user
        data['action'] = log.action

    return render(request, "./main/monitoring/log-window.html", data)


def logs(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/')

    data = {}
    logs = (Log.objects
            .annotate(day=TruncDay('date'))
            .values('day')
            .annotate(count=Count('id', distinct=True))
            .order_by('-date__day'))

    if 'key' in request.GET:
        logs = (Log.objects
                .annotate(day=TruncDay('date'))
                .values('day')
                .annotate(count=Count('id', distinct=+ True))
                .filter(search_field__icontains=request.GET['key'])
                .order_by('-date__day'))
        data['key'] = request.GET['key']

    data['logs'] = logs
    data['page'] = 'logs'

    return render(request, "./main/monitoring/logs.html", data)

def delete(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/')

    try:
        if request.GET['bulk'] == '1':
            Log.objects.filter(search_field = request.GET['params']).delete()
            messages.success(request, 'Log(s) deleted succesfully')
        else:
            print('I am here...')
            Log.objects.filter(id = int(request.GET['params'])).delete()
            messages.success(request, 'Log deleted succesfully')
            return redirect('/logs/'+str(request.GET['day']))
        
    except KeyError:
        messages.error(request, 'Something went wrong')
    
    return redirect('/logs')


def view_logs(request, day):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/')

    logs = Log.objects.filter(search_field = day).order_by('-date__day')

    data = {'logs': logs,
            'page': 'logs',
            'day': day}

    return render(request, "./main/monitoring/view-logs.html", data)

def inventory(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/')
    
    books = Book.objects.filter(is_archived=False)
    archived = Book.objects.filter(is_archived=True)
    reserved = Book.objects.filter(category__name='Reserve Circulation')
    
    data = {'books': books,
            'archived': archived,
            'reserved': reserved,
            'page': 'inventory'}
    
    return render(request, "./main/monitoring/inventory.html", data)
    