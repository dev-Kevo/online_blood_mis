from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

# app_name = 'core'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_user, name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('doctors/update_info/', views.doctor_update_info, name='doctor_update_info'),
    path('patients/update_info/', views.patient_update_info, name='patient_update_info'),
    path('patients/', views.patients, name='patient_dashboard'),
    

    # path('tailwind/', views.tailwind_test, name='tailwind_test'),
    path('about/', views.About.as_view(), name='about'),
    path('help/', views.FAQ.as_view(), name='help'),
    path('privacy/', views.Pricacy.as_view(), name='privacy'),
    path('terms/', views.Terms.as_view(), name='terms'),
]
