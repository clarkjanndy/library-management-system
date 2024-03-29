from django.http import JsonResponse
from django.db.models import Count, Sum
import json

from main.models import Log, Student, Teacher, Book, BorrowedBook, Fine

from datetime import datetime
# Create your views here.

def get_student_count(request):
    students = Student.objects.all().aggregate(count=Count('id'))
    return JsonResponse(students)


def get_teacher_count(request):
    teachers = Teacher.objects.all().aggregate(count=Count('id'))
    return JsonResponse(teachers)


def get_book_count(request):
    books = Book.objects.all()
    
    if 'query' in request.GET:
        books = books.filter(available_quan__lte = request.GET['query'])
    
    books=books.aggregate(count=Count('id'))    
    return JsonResponse(books)

def get_fines_sum(request):
    students = Fine.objects.all().aggregate(sum=Sum('amount'))
    return JsonResponse(students)


def visit_histogram(request):
    metrics = {
        'visits': Count('user'),
    }

    logs = Log.objects.values('date__month', 'date__year').annotate(**metrics).filter(action="has login").order_by( 'date__year')
   
    series = [log["visits"] for log in logs.iterator()]
    x_label = [datetime(log["date__year"], log["date__month"], 1) for log in logs.iterator()]

    data = {"series": series, "x_label": x_label}
    return JsonResponse(data, safe=True)

def inventory(request):
    data =None
    if request.GET['type'] == 'on-shelf':
        data = Book.objects.all().aggregate(count=Sum('available_quan'))       
    elif request.GET['type'] == 'on-cart':
        data = BorrowedBook.objects.filter(status = 'on-cart').aggregate(count=Count('id')) 
    elif request.GET['type'] == 'borrowed':
        data = BorrowedBook.objects.filter(status__in = ['borrowed', 'to-be-returned']).aggregate(count=Count('id')) 
    else:
        pass
    
    return JsonResponse(data, safe=True)

def notif_count(request):
    
    borrowed = BorrowedBook.objects.filter(user= request.user, status="borrowed")
    count = len([ele for ele in borrowed if ele.get_fine() > 0])
    
    return JsonResponse({'count': count}, safe=True)

