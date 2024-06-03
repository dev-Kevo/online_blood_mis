from django.http import HttpResponse
from django.shortcuts import render, redirect
from . models import CustomeUser
from core.forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
from django.contrib.auth import login, authenticate

def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user_type = form.cleaned_data['register_as']
            password = form.cleaned_data['password1']

            # Create a new user instance without saving it yet
            new_user = CustomeUser(username=username, email=email, password=password)


            if user_type == 'donor':
                new_user.is_donor = True
                new_user.is_patient = False
                new_user.is_doctor = False
                new_user.is_verified = False
            elif user_type == 'patient':
                new_user.is_patient = True
                new_user.is_donor = False
                new_user.is_doctor = False
                new_user.is_verified = False
            else:
                new_user.is_doctor = True
                new_user.is_donor = False
                new_user.is_patient = False
                new_user.is_verified = False


            # Save the user to the database
            new_user.save()

            # Authenticate the user after saving
            user = authenticate(username=username, password=password, email=email)
            login(request, user)
            if user_type == 'donor':
                login(request, user)
                return redirect('donor_dashboard')
            elif user_type == 'patient':
                login(request, user)
                return redirect('patient_dashboard')
            else:
                login(request, user)
                return redirect('doctors')

        # If form is not valid, it will be re-rendered with errors

    # For GET requests or if the form is not valid
    return render(request, 'authentication/register.html', {'form': form})


def login_user(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username)
            print(password)

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
    logout(request)
    return redirect('login')
    # return render(request, 'authentication/logged.html')

def doctor_update_info(request):

    return render(request, 'core/doctors_update_info.html')

def patient_update_info(request):

    return render(request, 'core/patients_update_info.html')

def donor_update_info(request):

    return render(request, 'core/donors_update_info.html')

def patients(request):
    user = request.user
    if user.is_verified:
        messages.success(request, "Verified Successfully")
    else:
        messages.error(request, 'You are not verified')
   
    return render(request, 'patients/patients.html')

def donors(request):
    user = CustomeUser.objects.filter(username=request.user)
    
    return render(request, 'donors/donor.html')

def doctors(request):

    return render(request, 'core/doctors.html')