from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Window
from django.db.models.functions import RowNumber
from django.db.models import Count, Sum

from django.core.exceptions import ObjectDoesNotExist

from main.utils import dummy

from main.models import MyUser, Book, BookCategory, BorrowedBook, Activity, Fine
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
        books = books.filter(
            publish_date__gte=f"{request.GET['publish_year']}-01-01")
        data['publish_year'] = request.GET['publish_year']

    data['page'] = 'books'
    data['categories'] = categories
    data['years'] = [str(year['publish_date__year']) for year in Book.objects.all(
    ).values('publish_date__year').distinct().order_by('-publish_date__year')]
    data['books'] = books

    return render(request, "./main/book/books.html", data)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/books')

    borrowed = BorrowedBook.objects.all().order_by('date_borrowed')
    borow_rankings = BorrowedBook.objects.values('book__category__name', 'book__title').filter(status__in=['borrowed', 'returned']).annotate(
        count=Count('book'),
        rank=Window(
            expression=RowNumber(),
            order_by='-count'
        ))[:10]
    
    view_rankings = Book.objects.all().annotate(
        count=Count('views'),
        rank=Window(
            expression=RowNumber(),
            order_by='-count'
        ))[:10]
    
    fines = Fine.objects.all().order_by('-date_collected')
    
    data = {"borrowed": borrowed,
            "borow_rankings": borow_rankings,
            "view_rankings": view_rankings,
            "fines": fines,
            "page": 'book-dashboard',}

    return render(request, "./main/book/book-dashboard.html", data)


def add(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/books')

    # get all categories
    categories = BookCategory.objects.all()
    if request.method == 'POST':
        # create book instance
        book = Book(
            barcode=request.POST['barcode'],
            title=request.POST['title'],
            authors=request.POST['authors'],
            preface=request.POST['preface'],
            category_id=request.POST['category_id'],
            condition=request.POST['condition'],
            available_quan=request.POST['available_quan'],
            is_archived=request.POST['is_archived'],
            publish_date=request.POST['publish_date'],
            publisher=request.POST['publisher']
        )
        if request.POST['preface'] == '':
            book.preface = dummy.DUMMY_TEXT
        # save book instance
        book.save()

        messages.success(request, 'Book added successfully')
        return redirect('/books')

    data = {
        'page': 'add-book',
        'categories': categories
    }

    return render(request, "./main/book/add-book.html", data)


def edit(request, barcode):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/books')

    # get all categories
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
        book.publisher = request.POST['publisher']

        book.save()

        messages.success(request, 'Book updated successfully')
        return redirect('/inventory')

    data = {
        'page': 'inventory',
        'categories': categories,
        'book': book
    }

    return render(request, "./main/book/edit-book.html", data)


def view(request, barcode):
    if not request.user.is_authenticated:
        return redirect('/')

    # get a book
    book = Book.objects.get(barcode=barcode)

    # add the user to the one that view the book
    if not book.views.filter(id_no=request.user.id_no).exists():
        book.views.add(request.user)

    more = Book.objects.filter(category=book.category).exclude(
        barcode=book.barcode)[:3]

    data = {
        'page': 'books',
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
    books = Book.objects.exclude(available_quan=0).filter(is_archived=False)
    # get borrower
    if 'borrower-id' in request.GET:
        try:
            borrower = MyUser.objects.get(id_no=request.GET['borrower-id'])

            # check if borrower has borrowed books
            status_to_check = ['borrowed', 'to-be-returned']
            if BorrowedBook.objects.filter(user=borrower, status__in=status_to_check).exists():
                messages.error(
                    request, 'That user already have borrowed books. Please return all the books before borrowing again.')
                return redirect('/borrow-book')

            # get book to be borrowed
            if 'barcode' in request.GET:
                book = None
                try:
                    # try something
                    book = books.get(barcode=request.GET['barcode'])
                    print(book)
                except ObjectDoesNotExist:
                    messages.error(request, 'Book does not exists.')
                    return redirect('/borrow-book?borrower-id='+str(borrower.id_no))

                # add borrowed book to borrower
                if len(BorrowedBook.objects.filter(user=borrower).exclude(status='returned')) < 3:
                    BorrowedBook(user=borrower, book=book,
                                 status='on-cart').save()
                    # update book quantity
                    book.available_quan = book.available_quan - 1
                    book.save()
                else:
                    messages.error(request, 'Maximum book reached.')

                return redirect('/borrow-book?borrower-id='+str(borrower.id_no))

            # get entry to be returned
            if 'bor-id' in request.GET:
                to_be_returned = BorrowedBook.objects.get(
                    id=request.GET['bor-id'], status='on-cart', user=borrower)
                to_be_returned.book.available_quan = to_be_returned.book.available_quan + 1
                to_be_returned.book.save()

                to_be_returned.delete()
                return redirect('/borrow-book?borrower-id='+str(borrower.id_no))

            # updated values of borrowed book
            borrowed = BorrowedBook.objects.filter(
                user=borrower, status='on-cart').order_by('-date_borrowed')
            data['borrower'] = borrower
            data['borrowed'] = borrowed
        except:
            messages.error(request, 'Please Select a Borrower.')

    data['page'] = 'borrow-book'
    data['books'] = books

    return render(request, "./main/book/borrow-book.html", data)


def borrow_checkout(request, id_no):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/')

    borrower = MyUser.objects.get(id_no=id_no)
    # update all on-cart books to borrowed
    on_cart = BorrowedBook.objects.filter(user=borrower, status='on-cart')
    borrowed = BorrowedBook.objects.filter(user=borrower, status='borrowed')

    if BorrowedBook.objects.filter(user=borrower, status='on-cart'):
        on_cart.update(status='borrowed')
        response = {'success': True,
                    'message': 'Books borrowed successfuly. Print Borrower Slip ?'}

        Activity.objects.create(user=borrower, action='has borrowed books')
        messages.success(
            request, 'Books borrowed successfuly. Print Borrower Slip ?', extra_tags=str(borrower.id_no))
        return JsonResponse(response)
    elif borrowed:
        response = {'success': False,
                    'message': 'This user already have borrowed books.'}
        #  messages.error(request, 'This user already have borrowed books.')
    else:
        response = {'success': False, 'message': 'No Book Selected.'}
        # messages.error(request, 'No Book Selected.')
        return JsonResponse(response)
        # return redirect('/borrow-book?borrower-id='+str(borrower.id_no))

    return redirect('/borrow-book')


def print_borrower_slip(request, id_no):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/')

    # get all user borrowed books
    user = MyUser.objects.get(id_no=id_no)
    borrowed = BorrowedBook.objects.filter(user=user, status='borrowed')
    data = {'user': user,
            'borrowed': borrowed}

    return render(request, "./main/book/print-slip.html", data)


def return_book(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/')

    data = {}
    # get borrower
    if 'borrower-id' in request.GET:
        try:
            borrower = MyUser.objects.get(id_no=request.GET['borrower-id'])

            # get entry to be returned
            if 'bor-id' in request.GET and 'action' in request.GET:
                borrowed = BorrowedBook.objects.get(
                    id=request.GET['bor-id'], user=borrower)

                print(borrowed)

                if request.GET['action'] == '1':
                    borrowed.status = 'to-be-returned'
                else:
                    borrowed.status = 'borrowed'
                borrowed.save()

                return redirect('/return-book?borrower-id='+str(borrower.id_no))

            # updated values of borrowed book and to be returned books
            borrowed = BorrowedBook.objects.filter(
                user=borrower, status='borrowed').order_by('-date_borrowed')
            tbrs = BorrowedBook.objects.filter(
                user=borrower, status='to-be-returned').order_by('-date_borrowed')
            
            # get the total fines
            total_fines = sum([ele.get_fine() for ele in tbrs])

            data['borrower'] = borrower
            data['borrowed'] = borrowed  # borrowed books
            data['tbrs'] = tbrs  # to-be-return books
            data['fines'] = total_fines
        except:
            messages.error(request, 'Please Select a Borrower.')

    data['page'] = 'return-book'

    return render(request, "./main/book/return-book.html", data)


def return_checkout(request, id_no):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/')

    borrower = MyUser.objects.get(id_no=id_no)
    # update all pending books to borrowed
    tbr = BorrowedBook.objects.filter(user=borrower, status='to-be-returned')

    if tbr:
        # update each entry of the book
        for entry in tbr:
            entry.book.available_quan = entry.book.available_quan + 1
            entry.book.save()
            
        #insert an entry on Fine table    
        total_fine = sum([ele.get_fine() for ele in tbr])
    
        if total_fine > 0:
            Fine.objects.create(
                collected_from = borrower,
                amount = total_fine,    
                borrowed_book = [ele.book.id for ele in tbr]  
            )
        
        tbr.update(date_returned=datetime.now())
        tbr.update(status='returned')

        response = {'success': True,
                    'message': 'Books borrowed successfuly. Print Borrower Slip ?'}
        
        # insert an entry to activity table
        Activity.objects.create(user=borrower, action='has returned books')
        
        messages.success(request, 'Books successfuly returned!')
        return JsonResponse(response)
    else:
        response = {'success': False, 'message': 'No Book Selected.'}
        # messages.error(request, 'No Book Selected.')
        return JsonResponse(response)

    # return redirect('/return-book')
