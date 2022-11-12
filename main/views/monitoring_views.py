from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from main.models import MyUser, Logs

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
        last_log = Logs.objects.filter(user=user).last()

        action = 'has login'
        if last_log is not None:
            if last_log.action == 'has login':
                action = 'has logout'
            else:
                action = 'has login'

        log = Logs(
            user=user,
            date=datetime.now(),
            action=action,
            search_field = str(datetime.now().strftime('%B %d, %Y - %A'))
        )
        log.save()

        data['user'] = user
        data['action'] = log.action

    return render(request, "./main/monitoring/log-window.html", data)


def logs(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/')

    data = {}
    logs = (Logs.objects
            .annotate(day=TruncDay('date'))
            .values('day')
            .annotate(count=Count('id', distinct=True))
            .order_by('-date__day'))

    if 'key' in request.GET:
        logs = (Logs.objects
                .annotate(day=TruncDay('date'))
                .values('day')
                .annotate(count=Count('id', distinct=+ True))
                .filter(search_field__icontains = request.GET['key'])
                .order_by('-date__day'))
        data['key'] = request.GET['key']

    data['logs'] = logs
    data['page'] = 'logs'

    return render(request, "./main/monitoring/logs.html", data)
