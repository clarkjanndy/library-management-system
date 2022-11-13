from datetime import date
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from main.models import MyUser, Book, BookCategory

from main.utils import dummy

# Create your views here.
def books(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')
    
    data = {}
    categories = BookCategory.objects.all()
    books = Book.objects.all()
    
    if 'key' in request.GET:
         books = Book.objects.all().filter(title__icontains=request.GET['key'])
         data['key'] = request.GET['key']
    
    if 'filter' in request.GET:
         books = Book.objects.all().filter(category__name=request.GET['filter'], title__icontains=request.GET['key'])
         data['filter'] = request.GET['filter']
     
    data['page'] = 'books' 
    data['categories'] = categories
    data['books'] = books 
     
    return render(request, "./main/book/books.html", data)

def add(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/myprofile')
    
    #get all categories
    categories = BookCategory.objects.all()
    if request.method == 'POST':
        #create book instance
        book = Book(
            barcode = request.POST['barcode'],
            title = request.POST['title'],
            authors = request.POST['authors'],
            preface = request.POST['preface'],
            category_id = request.POST['category_id'],
            old_quan = request.POST['old_quan'],
            new_quan = request.POST['new_quan'],
            available_quan = request.POST['available_quan']
        )
        if  request.POST['preface'] == '':
            book.preface = dummy.DUMMY_TEXT
        #save book instance
        book.save()
        
        messages.info(request, 'Book added successfully')
        return redirect('/books')
        
    data={
        'page' : 'add-book',
        'categories': categories
    }
    
    return render(request, "./main/book/add-book.html", data)


def view(request, barcode):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/myprofile')
    
    #get a book
    book = Book.objects.get(barcode=barcode)
    more = Book.objects.filter(category = book.category).exclude(barcode = book.barcode)      
      
    data={
        'page' : 'books',
        'book': book,
        'more': more
    }
    
    return render(request, "./main/book/view-book.html", data)

