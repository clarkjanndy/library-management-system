from django.contrib import admin
from django.urls import path, include

from .views import action_views, validation_views, analytics_views

urlpatterns = [
    #validations
    path('validate-id-no', validation_views.validate_id_no, name="validate-id-no"),
    path('validate-barcode', validation_views.validate_barcode, name="validate_barcode"),
    
    #analytics
    path('get-student-count', analytics_views.get_student_count, name="get_student_count"),
    path('get-teacher-count', analytics_views.get_teacher_count, name="get_teacher_count"),
    path('get-book-count', analytics_views.get_book_count, name="get_book_count"),
    
    path('visit-histogram', analytics_views.visit_histogram, name="visit_histogram"),
]
