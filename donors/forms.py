
from django import forms
from django.forms import ModelForm
from donors.models import DonorAppointment, Donor, DonorSettings
from django.core.exceptions import ValidationError
from datetime import datetime, time


class DonorUpdateFormOne(ModelForm):
    
    class Meta:
        model = Donor
        fields = [
            'profile_photo',
            'id_number',
            'gender',
            'blood_group',
            'phone_number',
            'donation_location',
            'address',
            'weight_kg',
        ]

        widgets = {
            'profile_photo': forms.FileInput(attrs={'class': 'block w-full border border-gray-300  text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),
            
            'id_number': forms.TextInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'gender': forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'blood_group': forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'phone_number': forms.TextInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'donation_location': forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'address': forms.TextInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'weight_kg': forms.NumberInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }

class DonorUpdateForm(ModelForm):
    
    class Meta:
        model = Donor
        fields = [
            'profile_photo',
            'id_number',
            'gender',
            'blood_group',
            'phone_number',
            'donation_location',
            'type_donation',
            'address',
            'weight_kg',
        ]

        widgets = {
            'profile_photo': forms.FileInput(attrs={'class': 'block w-full border border-gray-300  text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),
            
            'id_number': forms.TextInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'gender': forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'blood_group': forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'phone_number': forms.TextInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'donation_location': forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'type_donation': forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'address': forms.TextInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            
            'weight_kg': forms.NumberInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }

class MakeAppointmentForm(forms.ModelForm):
    class Meta:
        model = DonorAppointment
        fields = ['date', 'time', 'beneficiary']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-input block rounded w-full mt-1', 'type': 'date', 'name': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-input block rounded w-full mt-1', 'type': 'time', 'name': 'time'}),
            'beneficiary': forms.TextInput(attrs={'class': 'form-textarea block rounded w-full mt-1', 'name': 'beneficiary'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('date')
        appointment_time = cleaned_data.get('time')

        # Check if the date is ahead of the current date
        if appointment_date and appointment_date <= datetime.now().date():
            self.add_error('date', 'The date must be in the future.')

        # Check if the time is between 8 AM and 4 PM
        if appointment_time:
            if not (time(8, 0) <= appointment_time <= time(16, 0)):
                self.add_error('time', 'The time must be between 8 AM and 4 PM.')

        return cleaned_data

class UpdateDonorAfterDonationForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [
            'amount_of_donation',
            'blood_group',
            'type_donation',
            'weight_kg',
        ]


        widgets = {

            'amount_of_donation': forms.NumberInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'blood_group': forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'type_donation': forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'weight_kg': forms.NumberInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

        }

class DonorSettingsForm(forms.ModelForm):
    class Meta:
        model = DonorSettings
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