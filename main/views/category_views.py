
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Count

from django.contrib import messages

from main.models import Book, BookCategory
# Create your views here.


def categories(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/books')

    categories = BookCategory.objects.all()
    
    categories_with_count = []
    
    for cat in categories:
        categories_with_count.append({
            "id": cat.id,
            "name": cat.name,
            "get_limit_str": cat.get_limit_str,
            "get_rate_str": cat.get_rate_str,
            "book_count": Book.objects.filter(category = cat).aggregate(count=Count('id')).get('count')
        })
   
    data = {
        "categories":categories_with_count,
        "page": "book-categories"
    }
    return render(request, "./main/category/categories.html", data)

def add(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/books')
    
    if request.method == 'POST':
        BookCategory.objects.create(name = request.POST['name'],
                                   limit = request.POST['limit'],
                                   rate = request.POST['rate'] )

        messages.success(request, 'Category added successfully')
        return redirect('/book-categories')

    data = {
        'page': 'book-categories',
    }

    return render(request, "./main/category/add-category.html", data)


def edit(request, id):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/books')
    
    category = BookCategory.objects.get(id=id)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.limit = request.POST['limit']
        category.rate = request.POST['rate']
        category.save()

        messages.success(request, 'Category updated successfully')
        return redirect('/book-categories')

    data = {
        'page': 'book-categories',
        'category': category,
    }

    return render(request, "./main/category/edit-category.html", data)