from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.MyUser)
admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Log)
admin.site.register(models.BookCategory)
admin.site.register(models.Book)
admin.site.register(models.BorrowedBook)
admin.site.register(models.Fine)
admin.site.register(models.Activity)