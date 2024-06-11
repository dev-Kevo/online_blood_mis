from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from donors.forms import DonorUpdateForm
from donors.models import Donor
from patients.forms import PatientUpdateForm
from patients.models import Patient
from django.contrib import messages





@login_required
def index(request):
    """
    Doctors Dashboard
    """

    donors = Donor.objects.count()
    patients = Patient.objects.count()
    total_donations  = Donor.get_total_donations()


    context = {
        "donors" : donors,
        "patients" : patients,
        "total_donations" : total_donations,
    }
    
    return render(request, 'doctors/doctors.html', context)

def donor_management(request):
    """
    A view that will list all the Registered Donors
    """

    donors = Donor.objects.all()

    context = {
        "donors" : donors,
       
    }

    return render(request, 'doctors/donor_list.html', context)

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


def patient_management(request):
    """
    A view that will list all the Registered Patients
    """

    patients = Patient.objects.all()

    context = {
        "patients" : patients,
       
    }

    return render(request, 'doctors/patient_list.html', context)


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

def doctor_settings(request):
    context = {}
    
    return render(request, 'doctors/settings.html',context)