from django.utils import timezone
import random
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from doctors.models import Doctor, DoctorAppointments, DoctorNotification
from patients.forms import PatientUpdateForm, MakeAppointmentForm
from patients.models import PatientDonations, Patient, PatientAppointment
from django.db.models import Sum



@login_required
def patients(request):
    """
    Patients Dashboard
    """
    user = request.user
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

                    if selected_doctor.no_appointments >= 20:
                        selected_doctor.is_available = False
                        selected_doctor.save()
                    else:
                        selected_doctor.is_available = True
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

def patient_appointments(request):
    """
    List of all appointments
    """
    user = request.user
    appointments = PatientAppointment.objects.filter(patient=user).order_by('-created')
    doctors = Doctor.objects.filter(is_available=True)
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

                    if selected_doctor.no_appointments >= 20:
                        selected_doctor.is_available = False
                        selected_doctor.save()
                    else:
                        selected_doctor.is_available = True
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
                messages.error(request, "Form submission failed. Please check the form data.")

    else:
        appointment_form = MakeAppointmentForm()

    context = {
        'appointments': appointments,
        'appointments_form': appointment_form
    }

    return render(request, 'patients/patient_appointments.html', context)
