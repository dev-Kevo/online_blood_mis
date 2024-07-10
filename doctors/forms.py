from patients.models import PatientDonations
from .models import Doctor, DoctorSettings
from django import forms
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from core.models import CustomUser


class DoctorRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('doctor', 'Doctor'),
    ]

    username = forms.CharField(widget=forms.TextInput(attrs={"class" : "username"}), required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={"class" : "username"}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'password1'}), required=True, label='Set Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'password1'}), required=True, label='Confirm Password')
    # register_as = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, required=True, )
    
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

class UpadateDoctorInfo(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'license_number',
            'specialty',
            'hospital_affiliated',
        ]

        widgets = {
            'license_number': forms.TextInput(
                attrs={
                    'class': 'form-input mb-3 block w-full rounded border-gray-300 shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                    'placeholder': 'Your Licence Number',
                    'type': 'text',
                    }
                ),
            'specialty': forms.Select(
                attrs={
                    'class': 'form-textarea mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', 
                    # 'placeholder': 'Speciality',
                    # 'type' : 'text'
                    }
                ),

            'hospital_affiliated': forms.TextInput(
                attrs={
                    'class': 'form-input mb-3 block w-full rounded border-gray-300 shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                    'type': 'date',
                    'placeholder': 'Hospital Affiliated',
                    'type' : 'text'
                    }
                ),
        }

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
                    'placeholder': 'Amount of blood Used (Bags)',
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
    
    def clean(self):
        cleaned_data = super().clean()
        amount_of_blood_used = cleaned_data.get("amount_of_blood_used")
        follow_up_date = cleaned_data.get("follow_up_date")

        if not amount_of_blood_used and not follow_up_date:
            self.add_error('amount_of_blood_used', 'Amount of blood used is required')
            self.add_error('follow_up_date', 'Follow up date is required')

        if amount_of_blood_used and amount_of_blood_used < 0:
            self.add_error('amount_of_blood_used', 'Amount of blood used cannot be negative')
        
        if follow_up_date and follow_up_date < datetime.today().date():
            self.add_error('follow_up_date', 'Follow up date cannot be in the past')
        
        return cleaned_data
    
class UpdateDoctorMaxAppointments(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['number_max_appointments']     