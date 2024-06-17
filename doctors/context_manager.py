from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from doctors.models import Doctor, DoctorNotification
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def context(request):
    user = request.user
    doctor = None
    no_notification = 0
    notification_messages = []

    if user.is_authenticated and user.is_doctor:
        doctor = Doctor.objects.get(user=user)
        no_notification = DoctorNotification.objects.filter(doctor=doctor, is_read=False).count()
        notification_messages = DoctorNotification.objects.filter(doctor=doctor, is_read=False)

    context = {
        'no_notification': no_notification,
        'notification_messages': notification_messages,
    }

    return context

@login_required
def notification(request, pk):
    notification = get_object_or_404(DoctorNotification, pk=pk)
    notification.is_read = True
    notification.save()
    return messages.success(request, "Notification read successfully")
