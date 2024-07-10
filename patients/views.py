from django.utils import timezone
import random
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from doctors.models import Doctor, DoctorAppointments, DoctorNotification
from patients.forms import PatientUpdateForm, MakeAppointmentForm, PatientUpdateProfileForm, PatientSettingsForm
from patients.models import PatientDonations, Patient, PatientAppointment, PatientSettings
from django.db.models import Sum



@login_required
def patients(request):
    """
    Patients Dashboard
    """
    user = request.user
    if not user.is_patient:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')
    
    patient = Patient.objects.get(user=user)
    doctors = Doctor.objects.filter(is_available=True)
    recent_donations = PatientDonations.objects.filter(patient=user).order_by('-created')[:5]
    total_blood_charge = recent_donations.count()
    total_donated_bood = PatientDonations.objects.filter(patient=user).aggregate(total=Sum('amount_of_blood_used'))['total'] or 0
    upcoming_appointments = PatientAppointment.objects.filter(patient=user, status = 'PENDING', date__gte=timezone.now()).order_by('created')


    if patient.user.is_verified:
        appointment_form = MakeAppointmentForm()

        if request.method == 'POST':
            appointment_form = MakeAppointmentForm(request.POST)

            if appointment_form.is_valid():
                date = appointment_form.cleaned_data['date']
                time = appointment_form.cleaned_data['time']
                location = appointment_form.cleaned_data['location']
               
                if doctors:
                    selected_doctor = random.choice(doctors)
                    
                    appointment = PatientAppointment.objects.create(
                        patient=user,
                        date=date,
                        time=time,
                        location=location
                    )
                    appointment.save()

                    if selected_doctor.get_availability_status:
                        doctors_appointment = DoctorAppointments.objects.create(
                            doctor=selected_doctor,
                            patient=patient,
                            date=date,
                            time=time
                        )
                        doctors_appointment.save()
                        selected_doctor.update_no_appointments('add')
                        selected_doctor.save()

                        doctors_notification = DoctorNotification.objects.create(
                            doctor=selected_doctor,
                            notify_from="Donor" if request.user.is_donor else "Patient",
                            message=f"{patient} will be donating blood on {date} at {time}"
                        )
                        doctors_notification.save()
                        messages.success(request, "Appointment created successfully. Visit your preferred donation location to donate.")
                        return redirect('patient_dashboard')
                    else:
                        messages.error(request, f"No doctors available at the moment, please try again later!")
                        return redirect('patient_dashboard')
                else:
                    messages.error(request, "No doctors available at the moment, please try again later!")
                    return redirect('patient_dashboard')
            else:
                messages.error(request, "Form submission failed. Please check the form data.")

        else:
            appointment_form = MakeAppointmentForm()


        context = {
            'patient': patient,
            'recent_donations': recent_donations,
            'total_blood_charge': total_blood_charge,
            'total_donated_bood': total_donated_bood,
            'upcoming_appointments': upcoming_appointments,
            'appointment_form': appointment_form,

        }

        return render(request, 'patients/patients.html', context)
    else:
        messages.error(request, "Please update your information to continue.")
        return redirect('patient_update_info')

@login_required  
def patient_update_info(request):
    """
    make sure the patient has updated the required information
    """

    """
    Ensure the donor has updated the required information.
    """
    user = request.user  # Get the logged-in user
    patient = Patient.objects.get(user=user)
   
    if request.method == 'POST':
        update_form = PatientUpdateForm(request.POST, request.FILES, instance=patient)
        if update_form.is_valid():
            update_form.save()
            user.is_verified = True
            user.save()
            messages.success(request, f"Thank you {user.username} for updating your information.")
            return redirect('patient_dashboard')
        else:
            messages.error(request, "There was an error updating your information. Please try again.")
    else:
        update_form = PatientUpdateForm(instance=patient)

    context = {
        'update_form': update_form,
        'patient' : patient,
        'user': user
    }
    
    return render(request, 'patients/patient_update_info.html', context)

@login_required
def patient_appointments(request):
    """
    List of all appointments
    """
    user = request.user
    appointments = PatientAppointment.objects.filter(patient=user).order_by('-created')
    doctors = Doctor.objects.filter(is_available=True)
    print(list(doctors))
    patient = Patient.objects.get(user=user)

    if request.method == 'POST':
            appointment_form = MakeAppointmentForm(request.POST)

            if appointment_form.is_valid():
                date = appointment_form.cleaned_data['date']
                time = appointment_form.cleaned_data['time']
                location = appointment_form.cleaned_data['location']
               
                if doctors:
                    selected_doctor = random.choice(doctors)
                    
                    appointment = PatientAppointment.objects.create(
                        patient=user,
                        date=date,
                        time=time,
                        location=location
                    )
                    appointment.save()

                    print(selected_doctor)

                    if selected_doctor.get_availability_status:
                        doctors_appointment = DoctorAppointments.objects.create(
                            doctor=selected_doctor,
                            patient=patient,
                            date=date,
                            time=time
                        )

                        doctors_appointment.save()

                        selected_doctor.update_no_appointments('add')
                        selected_doctor.save()

                        doctors_notification = DoctorNotification.objects.create(
                            doctor=selected_doctor,
                            notify_from="Donor" if request.user.is_donor else "Patient",
                            message=f"{patient} will be donating blood on {date} at {time}"
                        )
                        doctors_notification.save()

                        messages.success(request, "Appointment created successfully. Visit your preferred donation location to donate.")
                        return redirect('patient_dashboard')
                    else:
                        messages.error(request, "No doctors available at the moment, please try again later!")
                        return redirect('patient_dashboard')
                else:
                     messages.error(request, "No doctors available at the moment, please try again later!")
                     return redirect('patient_dashboard')
            else:
                messages.error(request, "Form submission failed. Please check the form data.")

    else:
        appointment_form = MakeAppointmentForm()

    context = {
        'appointments': appointments,
        'appointments_form': appointment_form
    }

    return render(request, 'patients/patient_appointments.html', context)


@login_required
def profile(request):
    """
    Patient profile
    """
    user = request.user
    patient = Patient.objects.get(user=user)
    profile_form = PatientUpdateProfileForm(instance=patient)

    if request.method == 'POST':
        profile_form = PatientUpdateProfileForm(request.POST, request.FILES, instance=patient)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('patient_profile')
        else:
            messages.error(request, "Profile update failed. Please check the form data.")

    else:
        profile_form = PatientUpdateProfileForm(instance=patient)

    context = {
        'patient': patient,
        'profile_form': profile_form
    }
    return render(request, 'patients/profile.html', context)


@login_required
def settings(request):
    """
    Patient settings
    """
    user = request.user
    patient = Patient.objects.get(user=user)
    patient_settings = PatientSettings.objects.get(patient=patient)

    settings_form = PatientSettingsForm(instance=patient_settings)

    if request.method == 'POST':
        settings_form = PatientSettingsForm(request.POST, instance=patient_settings)
        if settings_form.is_valid():
            settings_form.save()
            messages.success(request, "Settings updated successfully.")
            return redirect('patient_settings')
        else:
            messages.error(request, "Settings update failed. Please check the form data.")

    else:
        settings_form = PatientSettingsForm(instance=patient_settings)


    context = {
        'patient': patient,
        'settings_form': settings_form
    }

    return render(request, 'patients/settings.html', context)

@login_required
def reports(request):
    """
    Patient reports
    """
    user = request.user
    patient = Patient.objects.get(user=user)
    reports = PatientDonations.objects.filter(patient=user).order_by('-created')
    context = {
        'patient': patient,
        'reports': reports
    }
    return render(request, 'patients/reports.html', context)
