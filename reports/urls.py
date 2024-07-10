from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reports'),
    path('report_details/<int:report_id>/', views.report_details, name='report_details'),
    path('delete_report/<int:pk>/', views.delete_report, name='delete_report'),
    path('donation_report/', views.donation_report, name='donation_records'),
]