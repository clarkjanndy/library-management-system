from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from django.db.models import Count
from django.db.models import Window, F
from django.db.models.functions import RowNumber

from main.models import Log, Teacher, Student, BookCategory, Activity, BorrowedBook
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
        'user__ext_name').filter(action='has login').annotate(
            count=Count('user'),
            rank=Window(
                expression=RowNumber(),
                order_by='-count'
            ))[:10]
        
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
    
    borrowed = BorrowedBook.objects.filter(user= request.user, status="borrowed")
    fine_count = len([ele for ele in borrowed if ele.get_fine() > 0])
    
    data = {
        "page": 'my-profile',
        "borrowed": borrowed,
        "fine_count": fine_count
    }
    
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
