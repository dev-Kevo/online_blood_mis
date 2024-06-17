from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='doctors_dashboard'),
    path('donor_management/', views.donor_management, name='donor_management'),
    path('donor_management/<int:pk>/', views.donor_details, name='donor_details'),

    path('patient_management/', views.patient_management, name='patient_management'),
    path('patient_management/<int:pk>/', views.patient_details, name='patient_details'),

    path('appointments/', views.appointments, name='doc_appointments'),
    path('appointment/attend/<int:pk>/', views.appointment_attendance, name='appointment_attendance'),
    path('appointment/details/<int:pk>/', views.appointment_details, name='appointment_details'),
    path('read/<int:pk>/', views.read_notification, name='read_notification'),
    path('blood_inventory/', views.blood_inventory, name='blood_inventory'),
    path('donation_records/', views.donation_records, name='donation_records'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.doctor_settings, name='doctor_settings'),
]