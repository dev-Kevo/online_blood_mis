from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='doctors_dashboard'),
    path('donor_management/', views.donor_management, name='donor_management'),
    path('donor_management/<int:pk>/', views.donor_details, name='donor_details'),

    path('patient_management/', views.patient_management, name='patient_management'),
    path('patient_management/<int:pk>/', views.patient_details, name='patient_details'),

    path('appointments/', views.appointments, name='doc_appointments'),
    path('appointment/attend_patient/<int:pk>/', views.patient_appointment_attendance, name='patient_appointment_attendance'),
    path('appointment/patient/details/<int:pk>/', views.patient_appointment_detail, name='patient_appointment_detail'),
    path('appointment/attend_donor/<int:pk>/', views.donor_appointment_attendance, name='donor_appointment_attendance'),
    path('appointment/donor/details/<int:pk>/', views.donor_appointment_details, name='donor_appointment_details'),
    path('appointment/patient/details/<int:pk>/', views.patient_appointment_detail, name='patient_appointment_detail'), # This is a duplicate of the above line
    path('read/<int:pk>/', views.read_notification, name='read_notification'),
    path('blood_inventory/', views.blood_inventory, name='blood_inventory'),
    path('donation_records/', views.donation_records, name='donation_records'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.doctor_settings, name='doctor_settings'),
]