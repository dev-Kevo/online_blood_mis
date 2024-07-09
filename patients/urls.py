from django.urls import path
from . import views

urlpatterns = [
    path('', views.patients, name='patient_dashboard'),
    path('appointments/', views.patient_appointments, name='patient_appointments'),
    path('update_info/', views.patient_update_info, name='patient_update_info'),
]