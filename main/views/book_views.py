from datetime import date, datetime
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from main.models import MyUser, Book, BookCategory, BorrowedBook
from django.db.models import Q

from main.utils import dummy

# Create your views here.
def books(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    data = {}
    categories = BookCategory.objects.all()
    books = Book.objects.all().filter(is_archived=False)
    
    if 'key' in request.GET and not request.GET['key'] == '':
         books = books.filter(title__icontains=request.GET['key'])
         data['key'] = request.GET['key']
    
    if 'category' in request.GET and not request.GET['category'] == '':
         books = books.filter(category__name=request.GET['category'])
         data['category'] = request.GET['category']
         
    if 'publish_year' in request.GET and not request.GET['publish_year'] == '':
         books = books.filter(publish_date__gte = f"{request.GET['publish_year']}-01-01")
         data['publish_year'] = request.GET['publish_year']
         
     
    data['page'] = 'books' 
    data['categories'] = categories
    data['years'] = [ str(year['publish_date__year']) for year in Book.objects.all().values('publish_date__year').distinct().order_by('-publish_date__year')]
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
            available_quan = request.POST['available_quan'],
            is_archived = request.POST['is_archived'],
            publish_date = request.POST['publish_date']
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
        book.is_archived = request.POST['is_archived']
        book.publish_date = request.POST['publish_date']
        
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
    
    #add the user to the one that view the book
    if not book.views.filter(id_no=request.user.id_no).exists():
         book.views.add(request.user)
   
    more = Book.objects.filter(category = book.category).exclude(barcode = book.barcode)[:3]
         
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
            status_to_check = ['borrowed', 'to-be-returned']
            if BorrowedBook.objects.filter(user = borrower, status__in = status_to_check).exists():
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
         
    books = Book.objects.exclude(available_quan = 0).filter(is_archived=False)    
    data['page']= 'borrow-book'
    data['books']= books
    
    return render(request, "./main/book/borrow-book.html", data )

def borrow_checkout(request, id_no):
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

def return_book(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')
    
    data = {}
    #get borrower
    if 'borrower-id' in request.GET:
        try:
            borrower = MyUser.objects.get(id_no = request.GET['borrower-id']) 
            
            #get entry to be returned
            if 'bor-id' in request.GET and 'action' in request.GET:
                 borrowed = BorrowedBook.objects.get(id=request.GET['bor-id'])
                 
                 print(borrowed)
                 
                 if request.GET['action'] == '1':
                    borrowed.status = 'to-be-returned'
                 else:
                    borrowed.status = 'borrowed'
                 borrowed.save()

                 return redirect('/return-book?borrower-id='+str(borrower.id_no)) 
                
            #updated values of borrowed book and to be returned books
            borrowed = BorrowedBook.objects.filter(user=borrower, status='borrowed').order_by('-date_borrowed')
            tbrs = BorrowedBook.objects.filter(user=borrower, status='to-be-returned').order_by('-date_borrowed')
            
            data['borrower']= borrower
            data['borrowed']= borrowed #borrowed books
            data['tbrs']= tbrs #to-be-return books
        except:
            messages.error(request, 'Please Select a Borrower.')  
        
    data['page']= 'return-book'
   
    return render(request, "./main/book/return-book.html", data )

def return_checkout(request, id_no):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if not request.user.is_superuser:
        return redirect('/')
    
    borrower = MyUser.objects.get(id_no=id_no)
    #update all pending books to borrowed
    tbr=BorrowedBook.objects.filter(user = borrower, status = 'to-be-returned')
    
    if tbr:
        #update each entry of the book
        for entry in tbr:
            entry.book.available_quan =  entry.book.available_quan + 1
            entry.book.save()

        tbr.update(date_returned=datetime.now())
        tbr.update(status='returned')
            
        messages.success(request, 'Books successfuly returned!')  
    else:
        messages.error(request, 'No Book Selected.') 
        return redirect('/return-book?borrower-id='+str(borrower.id_no))
    
    return redirect('/return-book')