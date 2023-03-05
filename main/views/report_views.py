from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import get_template

from ..models import Book

from main.utils.pdf_generator import pdf_generator

from datetime import date


def print_book_inventory(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')
    
    books = Book.objects.filter(is_archived=False)
    archived = Book.objects.filter(is_archived=True)
    reserved = Book.objects.filter(category__name='Reserve Circulation')
    today=date.today()
    
    template = get_template('main/reports/print_book_inventory.html')
    context = {'books': books,
            'archived': archived,
            'reserved': reserved,
            'date': today}
    
    generator = pdf_generator(template, context) 
    pdf = generator.generate()
    
    
    response = HttpResponse(pdf.read(),content_type='application/pdf;')
    response['Content-Disposition'] = 'filename="my-policy.pdf"'
            
    return response
    
    
     
    