from django.urls import path
from . import views

urlpatterns = [
    path('', views.donors, name='donor_dashboard'),
    path('<int:pk>/profile', views.profile, name='donor_update_info'),
    path('update_info/', views.donor_update_info, name='donor_update_info'),
    path('appointments/', views.appointments, name='appointments'),
]
