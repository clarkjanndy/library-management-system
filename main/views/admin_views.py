from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from django.db.models import Count

from main.models import Log, Teacher, Student, BookCategory, Activity
# Create your views here.


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/books')

    rates = BookCategory.objects.all()
    recent_activities = Activity.objects.all().order_by('-date')[:10]
    visitors = Log.objects.values(
        'user__first_name',
        'user__middle_name',
        'user__last_name',
        'user__ext_name').filter(action='has login').annotate(count=Count('user')).order_by('-count')

    print(visitors)
    data = {
        'page': 'dashboard',
        'recent_activities': recent_activities,
        'visitors': visitors,
        'rates': rates
    }

    return render(request, "./main/admin/dashboard.html", data)


def my_profile(request):
    if not request.user.is_authenticated:
        return redirect('/')

    data = {}
    data['page'] = 'my-profile'
    try:
        # get teacher
        teacher = Teacher.objects.get(user=request.user)
        data['teacher'] = teacher
    except Teacher.DoesNotExist:
        # get student
        student = Student.objects.get(user=request.user,)
        data['student'] = student
        return render(request, "./main/student/profile.html", data)

    return render(request, "./main/teacher/profile.html", data)

    # if request.user.is_staff:
    #     return redirect('/teachers/{id_no}'.format(id_no=request.user.id_no))

    # return redirect('/students/{id_no}'.format(id_no=request.user.id_no))
