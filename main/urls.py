from django.urls import path, include
from . views import page_views

urlpatterns = [
    path('', page_views.landing, name="landing"),
    path('login', page_views.login, name="login"),
]
