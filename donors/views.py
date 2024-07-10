import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse
from doctors.models import DoctorAppointments, Doctor, DoctorNotification
from donors.models import DonorDonations, Donor, DonorAppointment, DonorSettings, Notification
from .forms import DonorUpdateForm, DonorUpdateFormOne, MakeAppointmentForm, DonorSettingsForm
from django.db.models import Sum
from django.db import transaction
from django.utils import timezone


@login_required
def donors_dashboard(request):
    """
    Donors Dashboard view function to display the donor's dashboard and handle the appointment creation. 
    """
    doctors = Doctor.objects.filter(is_available=True)
    user = request.user
    if not user.is_donor:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')
    donor = Donor.objects.get(user=user)
    recent_donations = DonorDonations.objects.filter(donor=donor).order_by('-created')[:5]
    total_donations = recent_donations.count()
    total_donated_amount = DonorDonations.objects.filter(donor=donor).aggregate(total=Sum('amount'))['total'] or 0
    upcoming_appointments = DonorAppointment.objects.filter(donor=user, date__gte=timezone.now()).order_by('created')

    if donor.user.is_verified: 
        appointment_form = MakeAppointmentForm()
        if request.method == 'POST':
            appointment_form = MakeAppointmentForm(request.POST)

            if appointment_form.is_valid():
                date = appointment_form.cleaned_data['date']
                time = appointment_form.cleaned_data['time']
                beneficiary = appointment_form.cleaned_data['beneficiary']
                location = donor.donation_location

                if doctors.exists():
                    selected_doctor = random.choice(doctors)
                    
                    appointment = DonorAppointment.objects.create(
                        donor=user,
                        date=date,
                        time=time,
                        beneficiary=beneficiary,
                        location=location
                    )
                    appointment.save()
                    if selected_doctor.no_appointments >= 5:
                        selected_doctor.is_available = False
                        selected_doctor.save()
                    else:
                        doctors_appointment = DoctorAppointments.objects.create(
                            doctor=selected_doctor,
                            donor=donor,
                            date=date,
                            time=time
                        )
                        doctors_appointment.save()
                        selected_doctor.update_no_appointments('add')
                        selected_doctor.save()

                        doctors_notification = DoctorNotification.objects.create(
                            doctor=selected_doctor,
                            notify_from="Donor" if request.user.is_donor else "Patient",
                            message=f"{donor} will be donating blood on {date} at {time}"
                        )
                        doctors_notification.save()

                    messages.success(request, "Appointment created successfully. Visit your preferred donation location to donate.")
                    return redirect('appointments')
                else:
                    messages.error(request, "No doctors available at the moment, please try again later!")
            else:
                messages.error(request, "Form submission failed. Please check the form data.")

        else:
            appointment_form = MakeAppointmentForm()


        context = {
            'donor': donor,
            'recent_donations': recent_donations,
            'total_donations': total_donations,
            'total_donated_amount': total_donated_amount,
            'upcoming_appointments': upcoming_appointments,
            'appointment_form': appointment_form,

        }

        return render(request, 'donors/donor.html', context)
    else:
        messages.error(request, "Please update your information to continue.")
        return redirect('donor_update_info')

@login_required
def profile(request, pk):
    user = request.user
    donor = get_object_or_404(Donor, pk=pk)
    total_donations = DonorDonations.objects.filter(donor=user).count()
    total_appointments = DonorAppointment.objects.filter(donor=user).count()

    update_form = DonorUpdateFormOne()
    if request.method == 'POST':
        update_form = DonorUpdateFormOne(request.POST, request.FILES, instance=donor)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, f"Information Updated successfully")
            return HttpResponseRedirect(reverse('donor_profile', args=[donor.id]))
    else:
        update_form = DonorUpdateFormOne(instance=donor)


    context = {
        "donor" : donor,
        'update_form' : update_form,
        'total_donations' : total_donations,
        'total_appointments' : total_appointments,
    }
    
    return render(request, 'donors/profile.html', context)

@login_required
@transaction.atomic
def appointments(request):
    """
    Display the donor's appointments and handle the appointment creation.
    """
    
    user = request.user
    donor = Donor.objects.get(user=user)
    appointments = DonorAppointment.objects.filter(donor_id=user.id).order_by('created')
    doctors = Doctor.objects.filter(is_available=True)

    if request.method == 'POST':
        appointment_form = MakeAppointmentForm(request.POST)

        if appointment_form.is_valid():
            date = appointment_form.cleaned_data['date']
            time = appointment_form.cleaned_data['time']
            beneficiary = appointment_form.cleaned_data['beneficiary']
            location = donor.donation_location

            if doctors.exists():
                selected_doctor = random.choice(doctors)

                print(selected_doctor.get_availability_status)

                if selected_doctor.get_availability_status: 
                    appointment = DonorAppointment.objects.create(
                        donor=user,
                        date=date,
                        time=time,
                        beneficiary=beneficiary,
                        location=location
                    )
                    appointment.save()

                
                    doctors_appointment = DoctorAppointments.objects.create(
                        doctor=selected_doctor,
                        donor=donor,
                        date=date,
                        time=time
                    )

                    doctors_appointment.save()
                    selected_doctor.update_no_appointments('add')
                    selected_doctor.save()

                    doctors_notification = DoctorNotification.objects.create(
                        doctor=selected_doctor,
                        notify_from="Donor" if request.user.is_donor else "Patient",
                        message=f"{donor} will be donating blood on {date} at {time}"
                    )
                    doctors_notification.save()
                    messages.success(request, "Appointment created successfully. Visit your preferred donation location to donate.")
                    return redirect('appointments')
                
                else:
                    messages.error(request, "No doctors available at the moment, please try again later!")
                    return redirect('appointments')
                         
            else:
                messages.error(request, "No doctors available at the moment, please try again later!")
        else:
            messages.error(request, "Form submission failed. Please check the form data.")

    else:
        appointment_form = MakeAppointmentForm()

    context = {
        'donor': donor,
        'appointments': appointments,
        'appointment_form': appointment_form,
    }
    return render(request, 'donors/appointments.html', context)

def donor_update_info(request):
    """
    Ensure the donor has updated the required information.
    """
    user = request.user  # Get the logged-in user
    donor = Donor.objects.get(user=user)
   
    if request.method == 'POST':
        update_form = DonorUpdateForm(request.POST, request.FILES, instance=donor)
        if update_form.is_valid():
            update_form.save()
            user.is_verified = True
            user.save()
            messages.success(request, f"Thank you {user.username} for updating your information.")
            return redirect('donor_dashboard')
        else:
            messages.error(request, "There was an error updating your information. Please try again.")
    else:
        update_form = DonorUpdateForm(instance=donor)

    context = {
        'update_form': update_form,
        'donor' : donor,
        'user': user
    }

    return render(request, 'donors/donors_update_info.html', context)

@login_required
def donor_report(request):
    """
    Display the donor's report
    """
    user = request.user
    donor = Donor.objects.get(user=user)
    donations = DonorDonations.objects.filter(donor=user)
    total_donations = donations.count()
    total_donated_amount = donations.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'donor': donor,
        'donations': donations,
        'total_donations': total_donations,
        'total_donated_amount': total_donated_amount,
    }

    return render(request, 'donors/donor_report.html', context)

@login_required
def donor_settings(request):
    """
    Display the donor's settings page and handle the update of some part of donor's information.
    """
    user = request.user
    donor = Donor.objects.get(user=user)
    donor_settings = DonorSettings.objects.get(donor=donor.user)

    settings_form = DonorSettingsForm()

    if request.method == 'POST':
        settings_form = DonorSettingsForm(request.POST, instance=donor_settings)
        if settings_form.is_valid():
            settings_form.save()
            messages.success(request, "Settings updated successfully.")
            return redirect('donor_settings')
        else:
            messages.error(request, "There was an error updating your settings. Please try again.")

    else:
        settings_form = DonorSettingsForm(instance=donor_settings)

    context = {
        'donor': donor,
        'settings_form': settings_form,

    }

    return render(request, 'donors/donor_settings.html', context)