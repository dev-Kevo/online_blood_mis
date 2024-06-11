from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='doctors_dashboard'),
    path('donor_management/', views.donor_management, name='donor_management'),
    path('donor_management/<int:pk>/', views.donor_details, name='donor_details'),

    path('patient_management/', views.patient_management, name='patient_management'),
    path('patient_management/<int:pk>/', views.patient_details, name='patient_details'),

    path('settings/', views.doctor_settings, name='doctor_settings'),
]