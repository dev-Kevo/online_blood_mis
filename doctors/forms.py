from .models import Appointments
from django import forms

class DoctorAppointmentsCreateForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = [
            
        ]