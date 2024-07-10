from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from doctors.decorators import doctor_required
from donors.models import DonorDonations
from .models import Report
from .forms import ReportForm
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404


@doctor_required
@login_required
def index(request):

    reports = Report.objects.all()
    report_form = ReportForm()

    if request.method == 'POST':
        report_form = ReportForm(request.POST)

        if report_form.is_valid():
            report_form.save()
            messages.success(request, 'Report generated successfully')
            return redirect('reports')
        else:
            messages.error(request, 'An error occurred while generating the report')
    else:
        report_form = ReportForm()

    context = {
        'reports': reports,
        'report_form': report_form,
    }   

    return render(request, 'reports/index.html', context)


@doctor_required
@login_required
def report_details(request, report_id):
    report = Report.objects.get(id=report_id)
    #update the report 
    if request.method == 'POST':
        report_form = ReportForm(request.POST, instance=report)
        if report_form.is_valid():
            report_form.save()
            messages.success(request, 'Report updated successfully')
            return redirect('report_details', report_id=report_id)
        else:
            messages.error(request, 'An error occurred while updating the report')
    else:
        report_form = ReportForm(instance=report)

        

    context = {
        'report': report,
        'report_form': report_form,
    }

    return render(request, 'reports/report_details.html', context)

@doctor_required
@login_required
def delete_report(request, pk):
    report = get_object_or_404(Report, id=pk)
    
    if request.method == "POST":
        report_title = report.report_type  # Store the report title before deletion
        report.delete()
        messages.success(request, f'You successfully deleted {report_title} Report')
        return redirect('reports')  
    
    return render(request, 'reports/report_confirm_delete.html', {'report': report})

@doctor_required
@login_required
def donation_report(request):
    donation_records = DonorDonations.objects.all()

    context = {
        'donation_records': donation_records
    }

    return render(request, 'reports/donation_report.html', context)
