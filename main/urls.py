from django.urls import path
from . views import page_views, admin_views, student_views, teacher_views

urlpatterns = [
    path('', page_views.landing, name="landing"),
    path('login', page_views.login, name="login"),

    path('dashboard', admin_views.dashboard, name="dashboard"),

    path('students', student_views.students, name="students"),
    path('students/add', student_views.add, name="add_student"),
    
    
    path('teachers', teacher_views.teachers, name="teachers"),
    path('teachers/add', teacher_views.add, name="add_teachers"),
    
    path('logout', page_views.logout, name="logout"),
]
