from django.contrib import admin
from django.urls import path, include

from .views import action_views, validation_views

urlpatterns = [
    
    path('validate-id-no', validation_views.validate_id_no, name="validate-id-no"),
    path('validate-barcode', validation_views.validate_barcode, name="validate_barcode"),
]
