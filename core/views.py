from django.http import HttpResponse
from django.shortcuts import render, redirect

from donors.models import Donor
from . models import CustomUser
from core.forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView


def register(request):
    """
    Register user and assign the relevant role
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user_type = form.cleaned_data['register_as']
            password = form.cleaned_data['password1']

            # Use the create_user method to create a new user with initial attributes set
            new_user = CustomUser.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                is_donor=(user_type == 'donor'),
                is_patient=(user_type == 'patient'),
                is_doctor=(user_type == 'doctor')
            )

            # Since the default is_verified is already False, no need to set it again
            new_user.save()
            
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, 'authentication/register.html', {'form': form})



def login_user(request):
    """
    Login the user based on his/her role
    """
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # print(username)
            # print(password)

            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_doctor:
                login(request, user)
                if user.is_verified:
                    return redirect("doctors_dashboard")
                return redirect('doctor_update_info')
            
            elif user is not None and user.is_patient:
                login(request, user)
                if user.is_verified:
                    return redirect("patient_dashboard")
                return redirect('patient_update_info')
            
            elif user is not None and user.is_donor:
                login(request, user)
                if user.is_verified:
                    return redirect("donor_dashboard")
                return redirect('donor_update_info')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'authentication/login.html', {'form': form})


def logout_user(request):
    """
    Log out the user
    """
    logout(request)
    return redirect('login')
    # return render(request, 'authentication/logged.html')

def doctor_update_info(request):
    """
    make sure the doctor has updated the required information
    """

    return render(request, 'core/doctors_update_info.html')

def patient_update_info(request):
    """
    make sure the patient has updated the required information
    """
    
    return render(request, 'core/patients_update_info.html')


@login_required
def patients(request):
    """
    Patients Dashboard
    """
    user = request.user
    if user == "AnonymousUser":
        return redirect('login')
    if user.is_verified:
        messages.success(request, "Verified Successfully")
    else:
        messages.error(request, 'You are not verified')
   
    return render(request, 'patients/patients.html')


def welcome(request):
    """
    This view will welcome the user and prompt for login
    """
    return render(request, 'core/main.html')

@login_required
def doctors(request):
    """
    Doctors Dashboard
    """

    donors = Donor.objects.count()
    print(donors)

    context = {
        "donors" : donors
    }
    
    return render(request, 'doctors/doctors.html', context)


class About(TemplateView):
    """
    the about page
    """
    template_name = "main/about.html"

class FAQ(TemplateView):
    """
    Frequent asked questions
    """
    template_name = "main/faq.html"      

class Pricacy(TemplateView):
    """
    the privace policy
    """
    template_name = "main/privacy.html" 


class Terms(TemplateView):
    """
    Terms and conditions of the Website
    """
    template_name = "main/terms.html"        
            