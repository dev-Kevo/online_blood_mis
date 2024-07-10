from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'report_type',
            'description',
        ]
        
        widgets = {
            'report_type': forms.Select(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 mb-5 rounded shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-textarea mb-3 block w-full rounded-md border-gray-300 shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', 'placeholder': 'Write your report here...'
                    }
                    ),
        }


