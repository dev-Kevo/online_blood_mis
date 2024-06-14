import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse
from doctors.models import DoctorAppointments, Doctor, DoctorNotification
from donors.models import Donations, Donor, DonorAppointment, Notification
from .forms import DonorUpdateForm, DonorUpdateFormOne, MakeAppointmentForm
from django.db.models import Sum
from django.db import transaction


@login_required
def donors(request):
    """
    Donors Dashboard
    """
    user = request.user
    donor = Donor.objects.get(user=user)
    recent_donations = Donations.objects.filter(donor=user).order_by('-created')[:5]
    total_donations = recent_donations.count()
    total_donated_amount = Donations.objects.filter(donor=user).aggregate(total=Sum('amount'))['total'] or 0
    upcoming_appointments = DonorAppointment.objects.filter(donor=user, date__gte=timezone.now()).order_by('created')

    appointment_form = MakeAppointmentForm()
    if request.method == 'POST':
        appointment_form = MakeAppointmentForm(request.POST)

        donor = donor
        date = request.POST.get('date')
        time = request.POST.get('time')
        beneficiary = request.POST.get('beneficiary')
        location = donor.donation_location

                
        appointment = DonorAppointment.objects.create(
            donor = user,
            date = date,
            time = time,
            beneficiary = beneficiary,
            location = location
        )

        appointment.save()
        messages.success(request, "An appointment created successfully, visit your preffered donation location to donate.")
        return redirect('donor_dashboard')
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


def profile(request, pk):
    user = request.user
    donor = get_object_or_404(Donor, pk=pk)
    total_donations = Donations.objects.filter(donor=user).count()
    total_appointments = DonorAppointment.objects.filter(donor=user).count()

    update_form = DonorUpdateFormOne()
    if request.method == 'POST':
        update_form = DonorUpdateFormOne(request.POST, request.FILES, instance=donor)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, f"Information Updated successfully")
            return HttpResponseRedirect(reverse('donor_update_info', args=[donor.id]))
    else:
        update_form = DonorUpdateFormOne(instance=donor)


    context = {
        "donor" : donor,
        'update_form' : update_form,
        'total_donations' : total_donations,
        'total_appointments' : total_appointments,
    }
    
    return render(request, 'donors/profile.html', context)

@transaction.atomic
def appointments(request):
    user = request.user
    donor = Donor.objects.get(user=user)
    appointments = DonorAppointment.objects.filter(donor_id=user.id).order_by('-created')
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
                
                appointment = DonorAppointment.objects.create(
                    donor=user,
                    date=date,
                    time=time,
                    beneficiary=beneficiary,
                    location=location
                )

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