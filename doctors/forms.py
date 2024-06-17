from .models import DoctorSettings
from django import forms



class DoctorSettingsForm(forms.ModelForm):
    class Meta:
        model = DoctorSettings
        fields = [
            'email_notifications',
            'sms_notifications',
            'default_notification_method',
            'push_notifications',
            ]

        
        widgets = {
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-indigo-600 mb-5 flex items-center'}),

            'sms_notifications': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-indigo-600 mb-5 flex items-center'}),

            'default_notification_method': forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 mb-5 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'push_notifications': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-indigo-600 mb-5 flex flex-row items-center'}),
        }
    
        