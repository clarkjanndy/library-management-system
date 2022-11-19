from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.http import JsonResponse
from django.db.models import Count
import json

from main.models import Logs, Student, Teacher, Book

from datetime import datetime
# Create your views here.


def get_student_count(request):
    students = Student.objects.all().aggregate(count=Count('id'))
    return JsonResponse(students)


def get_teacher_count(request):
    teachers = Teacher.objects.all().aggregate(count=Count('id'))
    return JsonResponse(teachers)


def get_book_count(request):
    books = Book.objects.all().aggregate(count=Count('id'))
    return JsonResponse(books)


def visit_histogram(request):
    metrics = {
        'visits': Count('user', distinct=True),
    }

    logs = Logs.objects.values('date__month', 'date__year').annotate(**metrics).order_by('date__month')

    print(logs)
   
    series = [log["visits"] for log in logs.iterator()]
    x_label = [datetime(log["date__year"], log["date__month"], 1) for log in logs.iterator()]

    data = {"series": series, "x_label": x_label}
    return JsonResponse(data, safe=True)
