import csv
from django.contrib import admin
from .models import Income
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter
from django.http import HttpResponse
@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'source_name', 'amount', 'date_received', 'status', 'notes_snippet', 'custom_actions')
    search_fields = ('user__email', 'source_name', 'status', 'notes')    
    list_filter = (('date_received', DateRangeFilter), 'status')

    fields = ('user', 'source_name', 'amount', 'date_received', 'status', 'notes')
    actions = ['mark_as_received', 'export_to_csv']
    
    def notes_snippet(self, obj):
        return f"{obj.notes[:50]}..." if obj.notes else "No Notes"
    notes_snippet.short_description = "Notes"

    def custom_actions(self, obj):
        """Action to the change or edit the user data."""
        return format_html(
            '<a class="button" style="background:black;" href="{}">View</a> <a class="button"  style="background:black;" href="{}">Edit</a>',
            f"/admin/finance/income/{obj.id}/change/",
            f"/admin/finance/income/{obj.id}/",
        )
    custom_actions.short_description = "Actions"

    def mark_as_received(self, request, queryset):
        """Admin action to mark 'pending 'incomes as 'Received'."""
        updated = queryset.update(status='Received')
        self.message_user(request, f"{updated} incomes marked as Received.")
    mark_as_received.short_description = "Mark selected incomes as Received"

    def export_to_csv(self, request, queryset):
        """Export selected records to CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="income_records.csv"'
        writer = csv.writer(response)
        writer.writerow(['User', 'Source Name', 'Amount', 'Date Received', 'Status', 'Notes'])
        for obj in queryset:
            writer.writerow([obj.user, obj.source_name, obj.amount, obj.date_received, obj.status, obj.notes])
        return response
    export_to_csv.short_description = "Export selected incomes to CSV"
