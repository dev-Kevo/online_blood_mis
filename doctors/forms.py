from patients.models import PatientDonations
from .models import DoctorSettings
from django import forms
from datetime import datetime



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


class PatientDonationUpdateForm(forms.ModelForm):
    class Meta:
        model = PatientDonations

        fields = [
            'amount_of_blood_used',
            'treatment_notes',
            'follow_up_date',
            ]
        
        widgets = {
            'amount_of_blood_used': forms.NumberInput(
                attrs={
                    'class': 'form-input mb-3 block w-full rounded border-gray-300 shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                    'placeholder': 'Amount of blood used in ml',
                    'type': 'number',
                    }
                ),
            'treatment_notes': forms.Textarea(
                attrs={
                    'class': 'form-textarea mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', 
                    'placeholder': 'Treatment notes',

                    }
                ),

            'follow_up_date': forms.DateInput(
                attrs={
                    'class': 'form-input mb-3 block w-full rounded border-gray-300 shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                    'type': 'date',
                    'placeholder': 'Follow up date',
                    'min': datetime.today().strftime('%Y-%m-%d'),
                    }
                ),
        }
    
        