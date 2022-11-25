from django.shortcuts import render

from django.http import JsonResponse
import json

from main.models import MyUser, Student, Teacher, Book

from django.contrib.auth.hashers import check_password

# Create your views here.

def validate_id_no(request):
    user = MyUser.objects.all().filter(id_no = request.GET['id_no'])
    if not user.exists():
         return JsonResponse({'valid': True})
    
    return JsonResponse({'valid': False})

def validate_barcode(request):
   book = Book.objects.all().filter(barcode = request.GET['barcode'])
   if not book.exists():
       return JsonResponse({'valid': True})
    
   return JsonResponse({'valid': False})

def validate_password(request):
   if not check_password(request.GET['password'], request.user.password):
        return JsonResponse({'valid': False})

   return JsonResponse({'valid': True})