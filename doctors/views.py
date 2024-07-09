from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.notifier import sent_sms
from doctors.context_manager import notification
from doctors.forms import DoctorSettingsForm, PatientDonationUpdateForm
from doctors.models import Doctor, DoctorNotification, DoctorAppointments, AppointmentStatus, DoctorSettings
from donors.checkers import is_donor_eligible_to_donate
from donors.forms import DonorUpdateForm, UpdateDonorAfterDonationForm
from donors.models import AppointmentStatus, DonorDonations, Donor, DonorAppointment
from patients.forms import PatientUpdateForm
from patients.models import Patient, PatientAppointment, PatientDonations
from django.contrib import messages
from datetime import date
from .decorators import doctor_required


@doctor_required
@login_required
def index(request):
    """
    Doctors Dashboard
    """
    user = request.user
    print(user.is_doctor)
    if user.is_doctor == False:
        messages.error(request, "You are not authorized to view this page")
        return HttpResponseRedirect(reverse('login'))

    donors = Donor.objects.count()
    patients = Patient.objects.count()
    total_donations  = Donor.get_total_donations()
    no_notification = DoctorNotification.objects.filter(is_read=False).count()
    no_appointments = DoctorAppointments.objects.filter(status='PENDING').count()


    context = {
        "donors" : donors,
        "patients" : patients,
        "total_donations" : total_donations,
        "no_notification" : no_notification,
        "no_appointments" : no_appointments,
    }
    
    return render(request, 'doctors/doctors.html', context)

@doctor_required
@login_required
def read_notification(request, pk):
    notification(request, pk)
    return HttpResponse({"Message" : "Notification Read success"})

@doctor_required
@login_required
def donor_management(request):
    """
    A view that will list all the Registered Donors
    """

    donors = Donor.objects.all()

    context = {
        "donors" : donors,
    }

    return render(request, 'doctors/donor_list.html', context)

@doctor_required
@login_required
def donor_details(request, pk):
    """
    Access Donors Information and modify if needed
    """

    donor = get_object_or_404(Donor, pk=pk)

    if request.method == 'POST':
        update_form = DonorUpdateForm(request.POST, request.FILES, instance=donor)
        if update_form.is_valid():
            
            update_form.save()
            messages.success(request, f"{donor.user.username} information Updated successfully")
            return HttpResponseRedirect(reverse('donor_details', args=[donor.id]))
    else:
        update_form = DonorUpdateForm(instance=donor)


    context = {
        "donor" : donor,
        'update_form' : update_form
    }

    return render(request, 'doctors/donor_details.html', context)

@doctor_required
@login_required
def patient_management(request):
    """
    A view that will list all the Registered Patients
    """

    patients = Patient.objects.all()

    context = {
        "patients" : patients,
       
    }

    return render(request, 'doctors/patient_list.html', context)

@doctor_required
@login_required
def patient_details(request, pk):
    """
    Access Patient's Information and modify if needed.
    """

    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        update_form = PatientUpdateForm(request.POST, request.FILES, instance=patient)
        if update_form.is_valid():
            
            update_form.save()
            messages.success(request, f"{patient.user.username} information Updated successfully")
            return HttpResponseRedirect(reverse('patient_details', args=[patient.id]))
    else:
        update_form = PatientUpdateForm(instance=patient)


    context = {
        "patient" : patient,
        'update_form' : update_form
    }

    return render(request, 'doctors/patient_details.html', context)

@doctor_required
@login_required
def appointments(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    appointments = DoctorAppointments.objects.filter(doctor=doctor)

    donor_appointments_count = DoctorAppointments.objects.filter(doctor=doctor, donor__isnull=False).count()
    patient_appointments_count = DoctorAppointments.objects.filter(doctor=doctor, patient__isnull=False).count()
    completed_appointments = DoctorAppointments.objects.filter(doctor=doctor, status='COMPLETED').count()
    pending_appointments = DoctorAppointments.objects.filter(doctor=doctor, status='PENDING').count()



    context = {
        'appointments' : appointments, 
        'donor_appointments_count' : donor_appointments_count, 
        'patient_appointments_count' : patient_appointments_count, 
        'completed_appointments' : completed_appointments,
        'pending_appointments' : pending_appointments,
    }
    
    return render(request, 'doctors/apointments.html',context)

@doctor_required
@login_required
def donor_appointment_attendance(request, pk):

    appointment = get_object_or_404(DoctorAppointments, pk=pk)
    user = request.user
    doctor = Doctor.objects.get(user=user)
    donor_update_form = UpdateDonorAfterDonationForm()
    donor = appointment.donor
    donor_appointment = DonorAppointment.objects.filter(donor=donor.user, date=appointment.date, status='PENDING').first()


    bye_msg= f'{doctor} would like to thank you on behalf of Avenue Hospital for donating blood, we look forward seeing you again, have a wonderful time!.'
    donor_number = str(appointment.donor.phone_number)
    cleaned_donor_phone_number = '+254'+ donor_number.split('0', maxsplit=1)[1] 

    if request.method == 'POST':
        donor_update_form = UpdateDonorAfterDonationForm(request.POST, instance=donor)
        
        if donor_update_form.is_valid():

            amount_of_donation = donor_update_form.cleaned_data['amount_of_donation']
            blood_amount = donor_update_form.cleaned_data['blood_amount']
            
            # create donor donations ---> for the purpose of reports
            donations = DonorDonations.objects.create(
                donor = donor.user,
                amount = amount_of_donation,
                blood_amount = blood_amount,
                beneficiary = donor_appointment.beneficiary,
                description = f'Donation to {donor_appointment.beneficiary}'
            )

            donations.save()

            # update donor.number_of_donations
            donor.update_no_of_donations()
            
            # upadate if the donor is eligible to donate for the next donation
            donor.is_eligible_to_donate = is_donor_eligible_to_donate(donor.pk)

            # update donor.last_donation_date
            donor.update_last_donation_date(date.today())
            donor.save()
            donor_update_form.save()

            # update the donor apointment status 
            donor_appointment.status =  AppointmentStatus.COMPLETED 
            donor_appointment.save()

            # update the Doctors apointment status 
            appointment.status = AppointmentStatus.COMPLETED
            appointment.save()

            # clear the doctors notification
            doctor_notification = DoctorNotification.objects.filter(is_read=False).first()
            doctor_notification.delete()
            doctor.save()

            return redirect('doc_appointments')
            
    
    else:
        donor_update_form = UpdateDonorAfterDonationForm(instance=donor)

    context = {
        'appointment' : appointment,
        'donor_update_form' : donor_update_form,
        'donor_appointment' : donor_appointment,
    }
    
    return render(request, 'doctors/apointment_attendance.html',context)


@doctor_required
@login_required
def patient_appointment_attendance(request, pk):
    appointment = get_object_or_404(DoctorAppointments, pk=pk)
    user = request.user
    doctor = Doctor.objects.get(user=user)
    patient = appointment.patient
    patient_appointment = PatientAppointment.objects.filter(patient=patient.user, date=appointment.date, status='PENDING').first()

    patient_donation_update_form = PatientDonationUpdateForm()

    if request.method == 'POST':
        patient_donation_update_form = PatientDonationUpdateForm(request.POST, instance=patient)
        
        if patient_donation_update_form.is_valid():
            amount_of_blood_used = patient_donation_update_form.cleaned_data['amount_of_blood_used']
            treatment_notes = patient_donation_update_form.cleaned_data['treatment_notes']
            follow_up_date = patient_donation_update_form.cleaned_data['follow_up_date']

            # create patient donations ---> for the purpose of reports
            donations = PatientDonations.objects.create(
                patient = patient.user,
                amount_of_blood_used = amount_of_blood_used,
                treatment_notes = f'{treatment_notes}',
                follow_up_date = f'{follow_up_date}'
            )

            donations.save()

            
            # update patient.last_donation_date
            patient.update_last_blood_charge_date(date.today())
            patient.save()
            patient_donation_update_form.save()

            # update the patient apointment status 
            patient_appointment.status =  AppointmentStatus.COMPLETED 
            patient_appointment.save()

            # update the Doctors apointment status 
            appointment.status = AppointmentStatus.COMPLETED
            appointment.save()

            # clear the doctors notification
            doctor_notification = DoctorNotification.objects.filter(is_read=False).first()
            doctor_notification.delete()
            doctor.save()

            return redirect('doc_appointments')

    context = {
        'appointment' : appointment,
        'patient_donation_update_form' : patient_donation_update_form,
        'patient_appointment' : patient_appointment,
    }


    return render(request, 'doctors/patient_appointment_attendance.html', context)

@doctor_required
@login_required
def patient_appointment_detail(request, pk):

    appointment = get_object_or_404(DoctorAppointments, pk=pk)
    patient = Patient.objects.get(user=appointment.patient.user)
    patient_appointment = PatientDonations.objects.filter(patient=patient.user, date=appointment.date)[0]
    donation_amount = PatientDonations.objects.filter(patient=patient.user, created=appointment.modified).last().amount_of_blood_used

    context = {
        'appointment' : appointment,
        'patient' : patient,
        'patient_appointment' : patient_appointment,
        'donation_amount' : donation_amount,
    }

    return render(request, 'doctors/patient_appointment_detail.html', context)    

@doctor_required
@login_required
def donor_appointment_details(request, pk):

    appointment = get_object_or_404(DoctorAppointments, pk=pk)
    donor = Donor.objects.get(user=appointment.donor.user)
    donor_appointment = DonorAppointment.objects.filter(donor=donor.user, date=appointment.date)[0]
    donation_amount = DonorDonations.objects.filter(donor=donor.user, created=appointment.modified).last().amount

    context = {
        'appointment' : appointment,
        'donor' : donor,
        'donor_appointment' : donor_appointment,
        'donation_amount' : donation_amount,
    }

    return render(request, 'doctors/appointment_detail.html', context)

@doctor_required
@login_required
def patient_appointment_detail(request, pk):

    appointment = get_object_or_404(DoctorAppointments, pk=pk)
    patient = Patient.objects.get(user=appointment.patient.user)
    patient_appointment = PatientDonations.objects.filter(patient=patient.user, created=appointment.created).first()
    amount_of_blood_used = PatientDonations.objects.filter(patient=patient.user, created=appointment.modified).last().amount_of_blood_used

    context = {
        'appointment' : appointment,
        'patient' : patient,
        'patient_appointment' : patient_appointment,
        'amount_of_blood_used' : amount_of_blood_used,
    }

    return render(request, 'doctors/patient_appointment_detail.html', context)

@doctor_required
@login_required
def blood_inventory(request):


    context = {}

    return render(request, 'doctors/blood_inventory.html', context)

@doctor_required
@login_required
def donation_records(request):


    context = {}

    return render(request, 'doctors/donation_records.html', context)

@doctor_required
@login_required
def reports(request):


    context = {}

    return render(request, 'doctors/reports.html', context)

@doctor_required
@login_required
def doctor_settings(request):
    """
    Doctor's Settings Page
    """
    user = request.user
    doctor = Doctor.objects.get(user=user)
    setting = DoctorSettings.objects.get(doctor=doctor)

    setting_form = DoctorSettingsForm(instance=setting)

    if request.method == 'POST':
        setting_form = DoctorSettingsForm(request.POST, instance=setting)
        if setting_form.is_valid():
            setting_form.save()
            messages.success(request, "Settings Updated Successfully")
            return HttpResponseRedirect(reverse('doctor_settings'))
    else:
        setting_form = DoctorSettingsForm(instance=setting)
    
    
    context = {
        'doctor' : doctor,
        'setting_form' : setting_form,
    }
    
    return render(request, 'doctors/settings.html',context)