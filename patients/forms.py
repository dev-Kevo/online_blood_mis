from datetime import datetime, time
from django import forms
from django.forms import ModelForm
from . models import Patient, PatientAppointment, PatientSettings

class MakeAppointmentForm(forms.ModelForm):
    class Meta:
        model = PatientAppointment
        fields = ['date', 'time', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-input block rounded w-full mt-1', 'type': 'date', 'name': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-input block rounded w-full mt-1', 'type': 'time', 'name': 'time'}),
            'location': forms.Select(attrs={'class': 'form-input block rounded w-full mt-1', 'name': 'location'}),
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

class PatientUpdateForm(ModelForm):
    class Meta:
        model = Patient
        fields = [
            'profile_photo',
            'id_number',
            'date_of_birth',
            'gender',
            'blood_group',
            'address',
            'phone_number',
            'medical_conditions',
            'weight_kg',
        ]

        widgets = {

            'profile_photo': forms.FileInput(attrs={'class': 'block w-full mb-5 border border-gray-300  text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),

            'id_number': forms.TextInput(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'address': forms.TextInput(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'date_of_birth': forms.DateInput(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'blood_group': forms.Select(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'gender': forms.Select(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'phone_number': forms.TextInput(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'medical_conditions': forms.TextInput(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'weight_kg': forms.TextInput(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

        }

class PatientUpdateProfileForm(ModelForm):
    class Meta:
        model = Patient
        fields = [
            'profile_photo',
            'id_number',
            'date_of_birth',
            'gender',
            'blood_group',
            'address',
            'phone_number',
            'weight_kg',
        ]

        widgets = {

            'profile_photo': forms.FileInput(attrs={'class': 'block w-full mb-5 border border-gray-300  text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),

            'id_number': forms.TextInput(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'address': forms.TextInput(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'date_of_birth': forms.DateInput(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'blood_group': forms.Select(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'gender': forms.Select(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'phone_number': forms.TextInput(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

            'weight_kg': forms.TextInput(attrs={'class': 'block w-full mb-5 px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),

        }

class PatientSettingsForm(forms.ModelForm):
    class Meta:
        model = PatientSettings
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