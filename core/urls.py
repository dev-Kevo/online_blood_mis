from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

# app_name = 'core'

urlpatterns = [
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_user, name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('doctors/update_info/', views.doctor_update_info, name='doctor_update_info'),
    path('patients/update_info/', views.patient_update_info, name='patient_update_info'),
    path('donors/update_info/', views.donor_update_info, name='donor_update_info'),
    path('', views.doctors, name='doctors_dashboard'),
    path('patients/', views.patients, name='patient_dashboard'),
    path('donors/', views.donors, name='donor_dashboard'),
]
