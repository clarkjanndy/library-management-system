from django.shortcuts import render

from django.http import JsonResponse
import json

from main.models import MyUser, Student, Teacher, Book

# Create your views here.

def validate_id_no(request):
    user = MyUser.objects.all().filter(id_no = request.GET['id_no'])
    print(user)
    if not user.exists():
         return JsonResponse({'valid': True})
    
    return JsonResponse({'valid': False})

def validate_barcode(request):
   book = Book.objects.all().filter(barcode = request.GET['barcode'])
   print(book)
   if not book.exists():
       return JsonResponse({'valid': True})
    
   return JsonResponse({'valid': False})