from datetime import date
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from main.models import MyUser, Book, BookCategory, BorrowedBook

from main.utils import dummy

# Create your views here.
def books(request):
    if not request.user.is_authenticated:
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
        return redirect('/books')
    
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
            condition = request.POST['condition'],
            available_quan = request.POST['available_quan']
        )
        if  request.POST['preface'] == '':
            book.preface = dummy.DUMMY_TEXT
        #save book instance
        book.save()
        
        messages.success(request, 'Book added successfully')
        return redirect('/books')
        
    data={
        'page' : 'add-book',
        'categories': categories
    }
    
    return render(request, "./main/book/add-book.html", data)

def edit(request, barcode):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/books')
    
    #get all categories
    categories = BookCategory.objects.all()
    
    book = Book.objects.get(barcode=barcode)
    if request.method == 'POST':
        book.barcode = request.POST['barcode']
        book.title = request.POST['title']  
        book.authors = request.POST['authors']
        book.preface = request.POST['preface']
        book.category_id = request.POST['category_id']
        book.condition = request.POST['condition']
        book.available_quan = request.POST['available_quan']
        
        book.save()
        
        messages.success(request, 'Book updated successfully')
        return redirect('/inventory')
        
    data={
        'page' : 'inventory',
        'categories': categories,
        'book': book
    }
    
    return render(request, "./main/book/edit-book.html", data)

def view(request, barcode):
    if not request.user.is_authenticated:
        return redirect('/')
    
    #get a book
    book = Book.objects.get(barcode=barcode)
    more = Book.objects.filter(category = book.category).exclude(barcode = book.barcode)      
      
    data={
        'page' : 'books',
        'book': book,
        'more': more
    }
    
    return render(request, "./main/book/view-book.html", data)

def borrow_book(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')
    
    data = {}
    
    #get borrower
    if 'borrower-id' in request.GET:
        try:
            borrower = MyUser.objects.get(id_no = request.GET['borrower-id']) 
            
            #check if borrower has borrowed books
            if BorrowedBook.objects.filter(user = borrower, status = 'borrowed').exists():
                messages.error(request, 'That user already have borrowed books. Please return all the books before borrowing again.') 
                return redirect('/borrow-book') 
            
             #get book to be borrowed
            if 'book-id' in request.GET:
                book = Book.objects.get(id=request.GET['book-id'])
                
                #add borrowed book to borrower
                if len(BorrowedBook.objects.filter(user=borrower).exclude(status='returned')) < 5:
                    BorrowedBook(user=borrower, book = book , status = 'on-cart').save()
                    #update book quantity
                    book.available_quan = book.available_quan - 1
                    book.save()
                else:
                    messages.error(request, 'Maximum book reached.')
                
                return redirect('/borrow-book?borrower-id='+str(borrower.id_no))
            
            #get entry to be returned
            if 'bor-id' in request.GET:
                 to_be_returned = BorrowedBook.objects.get(id=request.GET['bor-id'], status= 'on-cart')
                 to_be_returned.book.available_quan = to_be_returned.book.available_quan + 1
                 to_be_returned.book.save()
              
                 to_be_returned.delete()
                 return redirect('/borrow-book?borrower-id='+str(borrower.id_no)) 
                
            #updated values of borrowed book
            borrowed = BorrowedBook.objects.filter(user=borrower, status='on-cart').order_by('-date_borrowed')
            data['borrower']= borrower
            data['borrowed']= borrowed
        except:
            messages.error(request, 'Please Select a Borrower.')  
         
    books = Book.objects.exclude(available_quan = 0)    
    data['page']= 'borrow-book'
    data['books']= books
    
    return render(request, "./main/book/borrow-book.html", data )

def checkout(request, id_no):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')
    
    borrower = MyUser.objects.get(id_no=id_no)
    #update all pending books to borrowed
    on_cart=BorrowedBook.objects.filter(user = borrower, status = 'on-cart')
    borrowed=BorrowedBook.objects.filter(user = borrower, status = 'borrowed')
    
    if BorrowedBook.objects.filter(user = borrower, status = 'on-cart'):
        on_cart.update(status='borrowed')
        messages.success(request, 'Books borrowed successfuly. Print Borrower Slip ?', extra_tags=str(borrower.id_no))  
    elif borrowed:
         messages.error(request, 'This user already have borrowed books.') 
    else:
        messages.error(request, 'No Book Selected.') 
        return redirect('/borrow-book?borrower-id='+str(borrower.id_no))
    
    return redirect('/borrow-book')

def print_borrower_slip(request, id_no):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')
    
    #get all user borrowed books
    user = MyUser.objects.get(id_no=id_no)
    borrowed = BorrowedBook.objects.filter(user = user, status='borrowed')
    data = {'user':user,
            'borrowed':borrowed}
    
    return render(request, "./main/book/print-slip.html", data)