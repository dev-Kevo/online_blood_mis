from django.http import HttpResponse
from django.shortcuts import render, redirect
from . models import CustomUser
from core.forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView

# Create your views here.
from django.contrib.auth import login, authenticate

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

            # Use the create_user method to create a new user
            new_user = CustomUser.objects.create_user(username=username, email=email, password=password)

            # Set user type attributes based on form data
            if user_type == 'donor':
                new_user.is_donor = True
            elif user_type == 'patient':
                new_user.is_patient = True
            else:
                new_user.is_doctor = True

            # Ensure all user types have default values
            new_user.is_verified = False
            new_user.save()

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user type
                if user_type == 'donor':
                    return redirect('donor_dashboard')
                elif user_type == 'patient':
                    return redirect('patient_dashboard')
                else:
                    return redirect('doctors')

        # If the form is not valid, it will be re-rendered with errors
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

            user = authenticate(username=username, password=password)
            print(user)
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
                if user.is_verified:
                    return redirect("donor_update_info")
                return redirect('donor_dashboard')
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

def donor_update_info(request):
    """
    make sure the donor has updated the required information
    """

    return render(request, 'core/donors_update_info.html')

def patients(request):
    """
    Patients Dashboard
    """
    user = request.user
    if user.is_verified:
        messages.success(request, "Verified Successfully")
    else:
        messages.error(request, 'You are not verified')
   
    return render(request, 'patients/patients.html')

def donors(request):
    """
    Donors Dashboard
    """
    user = CustomUser.objects.filter(username=request.user)
    
    return render(request, 'donors/donor.html')


def doctors(request):
    """
    Doctors Dashboard
    """
    return render(request, 'core/doctors.html')


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
            