from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime, timedelta

from django.db.models import Count

# Create your models here.
class MyUser(AbstractUser):
    id_no = models.CharField(max_length=50, blank = False, null = False, unique=True, primary_key=True)
    photo = models.CharField(max_length=200, blank = False, null = False, default='default-profile.webp')
    middle_name = models.CharField(max_length=50, blank = True)
    ext_name = models.CharField(max_length=50, blank = True)
    gender = models.CharField(null = False, blank = False, max_length = 32)
    civil_status = models.CharField(null = False, blank = False, max_length = 32)
    address = models.CharField(blank = False, null = False, max_length=90)
    contact_no = models.CharField(max_length=50, blank = False, null=False, default = '09')  
    username = None

    USERNAME_FIELD = 'id_no'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.id_no

class Student(models.Model):
    user = models.OneToOneField(MyUser, on_delete = models.DO_NOTHING, null = True)
    course = models.CharField(blank = False, null = False, max_length=90)
    year = models.CharField(blank = False, null = False, max_length=90)
    section = models.CharField(blank = False, null = False, max_length=90)
    
    def __str__(self):
        return self.user
    

class Teacher(models.Model):
    user = models.OneToOneField(MyUser, on_delete = models.DO_NOTHING, null = False)
    designation = models.CharField(blank = False, null = False, max_length=90)
    year_of_exp = models.CharField(blank = False, null = False, max_length=90)
    advisory = models.CharField(blank = True, null = True, max_length=90)
    
    def __str__(self):
        return self.user

class Logs(models.Model):
    user = models.ForeignKey(MyUser, on_delete = models.DO_NOTHING, null = False)
    date = models.DateTimeField(null=False, blank=False, default=datetime.now)
    action = models.CharField(blank = False, null = False, max_length=15)
    search_field = models.CharField(blank = False, null = False, max_length=30)
    
    def __str__(self):
        return self.user

class BookCategory(models.Model):
    name = models.CharField(blank = False, null = False, max_length=90)
    limit = models.IntegerField(blank = False, null = False)
    rate = models.DecimalField(blank = False, null=False, decimal_places=2, max_digits=32)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    barcode = models.CharField(blank = False, null = False, max_length=90)
    category = models.ForeignKey(BookCategory, on_delete = models.DO_NOTHING, null = False)
    title = models.CharField(blank = False, null = False, max_length=90)
    authors = models.TextField(blank = False, null = False)
    preface = models.TextField(blank = False, null = False, default = 'No Preface')
    condition = models.CharField(blank = False, null = False, max_length=90)
    available_quan = models.IntegerField(blank = False, null = False)
    
    def __str__(self):
        return self.barcode
    
    def get_on_cart(self):
        on_cart = BorrowedBook.objects.filter(book=self, status='on-cart').aggregate(count=Count('id'))        
        return on_cart['count']

    def get_borrowed(self):
        on_cart = BorrowedBook.objects.filter(book=self, status='borrowed').aggregate(count=Count('id'))        
        return on_cart['count']

class BorrowedBook(models.Model):
    user = models.ForeignKey(MyUser, on_delete = models.DO_NOTHING, null = False)
    book = models.ForeignKey(Book, on_delete = models.DO_NOTHING, null = False)
    status = models.CharField(blank = False, null = False, max_length=300)
    date_borrowed = models.DateTimeField(null=False, blank=False, default=datetime.now)
    expected_return_date = models.DateTimeField(null=False, blank=False)
    date_returned = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.book.title
    
    def save(self, *args, **kwargs):
        self.expected_return_date = datetime.now() + timedelta(hours=self.book.category.limit)
        super(BorrowedBook, self).save(*args, **kwargs)

    def get_fine(self):
        multiplier = datetime.now() - self.expected_return_date
        fine = 0 
        if multiplier.days > 0:
            fine = self.book.category.rate * (multiplier.days * 24)
        return int(fine)

class Fine(models.Model):
    borrowedbook = models.OneToOneField(BorrowedBook, on_delete = models.DO_NOTHING, null = False)
    amount = models.ForeignKey(BookCategory, on_delete = models.DO_NOTHING, null = False)
    status = models.CharField(blank = False, null = True, max_length=300)
    date = models.DateTimeField(null=False, blank=False, default=datetime.now)
    
    def __str__(self):
        return self.user





