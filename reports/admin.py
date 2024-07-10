from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'created', 'modified')
    search_fields = ('report_type', 'created', 'modified')
    list_filter = ('report_type', 'created', 'modified')
    ordering = ('-created',)

