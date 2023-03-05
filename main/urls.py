from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . views import page_views, admin_views, report_views, student_views, teacher_views, book_views, monitoring_views, report_views

urlpatterns = [
    path('', page_views.landing, name="landing"),
    path('initialize', page_views.initialize, name="initialize"),
    path('login', page_views.login, name="login"),
    path('change-password', page_views.change_password, name="change_password"),
    
    
    path('dashboard', admin_views.dashboard, name="dashboard"),
    path('my-profile', admin_views.my_profile, name="my-profile"),
  

    #students
    path('students', student_views.students, name="students"),
    path('students/add', student_views.add, name="add_student"),
    path('students/<str:id_no>', student_views.profile, name="student_profile"),
    path('students/<str:id_no>/edit', student_views.edit, name="edit_student"),
    path('students/<str:id_no>/upload-photo', student_views.UpdatePhoto.as_view(), name="student_upload_photo"),
    
    #teachers
    path('teachers', teacher_views.teachers, name="teachers"),
    path('teachers/add', teacher_views.add, name="add_teachers"),
    path('teachers/<str:id_no>', teacher_views.profile, name="teacher_profile"),
    path('teachers/<str:id_no>/edit', teacher_views.edit, name="edit_teacher"),
     path('teachers/<str:id_no>/upload-photo', teacher_views.UpdatePhoto.as_view(), name="student_upload_photo"),
    
    #books
    path('books', book_views.books, name="teachers"),
    path('books/add', book_views.add, name="add_book"),
    path('books/<str:barcode>', book_views.view, name="view_book"),
    path('books/<str:barcode>/edit', book_views.edit, name="edit_book"),
    
    
    path('borrow-book', book_views.borrow_book, name="borrow_book"),
    path('borrow-book/checkout/<str:id_no>', book_views.borrow_checkout, name="borrow_checkout"),
    path('print-slip/<str:id_no>', book_views.print_borrower_slip, name="print_borrower_slip"),
    
    path('return-book', book_views.return_book, name="return_book"),
    path('return-book/checkout/<str:id_no>', book_views.return_checkout, name="return_checkout"),
    
    #monitoring
    path('log-window', monitoring_views.log_window, name="log_window"),
    path('logs', monitoring_views.logs, name="logs"),
    # path('logs/delete', monitoring_views.delete, name="delete_logs"), 
    path('logs/<str:day>', monitoring_views.view_logs, name="view_logs"),       
    
    path('inventory', monitoring_views.inventory, name="inventory"),       
    
    #reports
    path('reports/book-inventory', report_views.print_book_inventory, name="print_book_inventory"),   
    
    
    path('logout', page_views.logout, name="logout"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)