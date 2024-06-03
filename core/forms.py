from django.contrib.auth.forms import UserCreationForm
from django import forms
from core.models import CustomeUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomeUser
        fields = '__all__'

class RegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('donor', 'Donor'),
    ]

    username = forms.CharField(widget=forms.TextInput(attrs={"class" : "username"}), required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={"class" : "username"}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'password1'}), required=True, label='Set Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'password1'}), required=True, label='Confirm Password')
    register_as = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, required=True, )
    
    class Meta:
        model = CustomeUser
        fields = [
            'username',
            'email',
            'register_as',
            'password1',
            'password2',
        ]


class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"id":"username", 'name': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id":"password", 'name' : 'password'}))
        
class UpdateInforForm(forms.ModelForm):
    class Meta:
        model = CustomeUser
        fields = [
            'id_number',
            'phone_number',
            'next_of_kin',
            'next_of_kin_phone_number',
            'blood_group',
            # 'is_doctor',
            'is_patient',
            'is_donor',
        ]

        