from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . views import page_views, admin_views, student_views, teacher_views, book_views, monitoring_views

urlpatterns = [
    path('', page_views.landing, name="landing"),
    path('login', page_views.login, name="login"),

    path('dashboard', admin_views.dashboard, name="dashboard"),

    #students
    path('students', student_views.students, name="students"),
    path('students/add', student_views.add, name="add_student"),
    path('students/<str:id_no>', student_views.profile, name="student_profile"),
    path('students/<str:id_no>/edit', student_views.edit, name="edit_student"),
    
    #teachers
    path('teachers', teacher_views.teachers, name="teachers"),
    path('teachers/add', teacher_views.add, name="add_teachers"),
    
    #books
    path('books', book_views.books, name="teachers"),
    path('books/add', book_views.add, name="add_book"),
    path('books/<str:barcode>', book_views.view, name="view_book"),
    
    
    #monitoring
    path('log-window', monitoring_views.log_window, name="log_window"),
    path('logs', monitoring_views.logs, name="logs"),     
    
    path('logout', page_views.logout, name="logout"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)