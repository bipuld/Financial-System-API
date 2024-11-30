import csv
from django.contrib import admin
from .models import Income,Expense,Loan
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter
from django.http import HttpResponse
@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'source_name', 'amount', 'date_received', 'status', 'notes_text', 'custom_actions')
    search_fields = ('user__email', 'source_name', 'status', 'notes')    
    list_filter = (('date_received', DateRangeFilter), 'status')
    fields = ('user', 'source_name', 'amount', 'date_received', 'status', 'notes')
    actions = ['mark_received', 'export_to_csv']
    
    def notes_text(self, obj):
        return f"{obj.notes[:50]}..." if obj.notes else "No Notes"
    notes_text.short_description = "Notes"

    def custom_actions(self, obj):
        """Action to the change or edit the user data."""
        return format_html(
             '<a class="button" style="background:black; margin-right: 10px; padding: 5px 10px; display: inline-block;" href="{}">View</a>'
            '<a class="button" style="background:black; padding: 5px 10px; display: inline-block;" href="{}">Edit</a>',
            f"/admin/finance/income/{obj.id}/change/",
            f"/admin/finance/income/{obj.id}/",
        )
    custom_actions.short_description = "Actions"



    def mark_received(self, request, queryset):
        """Admin action to mark 'pending 'incomes as 'Received'."""
        updated = queryset.update(status='Received')
        self.message_user(request, f"{updated} incomes marked as Received.")
    mark_received.short_description = "Mark selected incomes as Received"

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


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display=('user', 'category', 'amount', 'due_date', 'status', 'notes_text', 'custom_actions')
    search_fields = ('user__email', 'category', 'status', 'notes')
    list_filter = (('due_date', DateRangeFilter), 'status')
    fields = ('user', 'category', 'amount', 'due_date', 'status', 'notes')
    actions = ['mark_paid', 'export_to_csv']

    def notes_text(self, obj):
        return f"{obj.notes[:50]}..." if obj.notes else "No Notes"
    
    def custom_actions(self, obj):
        """Action to the change or edit the user data."""
        return format_html(
             '<a class="button" style="background:black; margin-right: 10px; padding: 5px 10px; display: inline-block;" href="{}">View</a>'
            '<a class="button" style="background:black; padding: 5px 10px; display: inline-block;" href="{}">Edit</a>',
            f"/admin/finance/expense/{obj.id}/change/",
            f"/admin/finance/expense/{obj.id}/",
        )
    custom_actions.short_description = "Actions"

    
    def mark_paid(self, request, queryset):
        """Admin action to mark 'Pending' Expenses as 'Paid'."""
        updated = queryset.update(status='Paid')
        self.message_user(request, f"{updated} Expenses marked as Paid.")
    mark_paid.short_description = "Mark selected Expenses as paid"

    
    def export_to_csv(self, request, queryset):
        """Export selected records to CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Expenses_record.csv"'
        writer = csv.writer(response)
        writer.writerow(['User', 'Category', 'Amount', 'Due Date', 'Status', 'Notes'])
        for obj in queryset:
            writer.writerow([obj.user, obj.category, obj.amount, obj.due_date, obj.status, obj.notes])
        return response
    export_to_csv.short_description = "Export selected Expenses to CSV"



@admin.register(Loan)
class LoadAdmin(admin.ModelAdmin):
    list_display = ('user', 'loan_name', 'principal_amount', 'remaining_balance', 'monthly_installment', 'status','notes','date_borrowed','custom_actions')
    readonly_fields = ('monthly_installment', 'remaining_balance')
    search_fields = ('user__email', 'loan_name', 'status', 'notes')
    list_filter = ('monthly_installment', 'status')
    actions = ['mark_paid', 'export_to_csv']
    def custom_actions(self, obj):
        """Action to the change or edit the user laon data."""
        return format_html(
             '<a class="button" style="background:black; margin-right: 10px; padding: 5px 10px; display: inline-block;" href="{}">View</a>'
            '<a class="button" style="background:black; padding: 5px 10px; display: inline-block;" href="{}">Edit</a>',
            f"/admin/finance/loan/{obj.id}/change/",
            f"/admin/finance/loan/{obj.id}/",
        )
    custom_actions.short_description = "Actions"

    def custom_actions(self, obj):
        """Action to the change or edit the user data."""
        return format_html(
             '<a class="button" style="background:black; margin-right: 10px; padding: 5px 10px; display: inline-block;" href="{}">View</a>'
            '<a class="button" style="background:black; padding: 5px 10px; display: inline-block;" href="{}">Edit</a>',
            f"/admin/finance/loan/{obj.id}/change/",
            f"/admin/finance/loan/{obj.id}/",
        )
    custom_actions.short_description = "Actions"
    def mark_paid(self, request, queryset):
        """Admin action to mark 'Active' Loans as 'Paid'."""
        updated = queryset.update(status='Paid')
        self.message_user(request, f"{updated} Loans marked as Paid.")


    def export_to_csv(self, request, queryset):
        """Export selected records to CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Loan_record.csv"'
        writer = csv.writer(response)
        writer.writerow(['User', 'Loan Name', 'Principal Amount', 'Remaining Balance', 'Monthly Installment', 'Status', 'Notes', 'Date Borrowed'])
        for obj in queryset:
            writer.writerow([obj.user, obj.loan_name, obj.principal_amount, obj.remaining_balance, obj.monthly_installment, obj.status, obj.notes, obj.date_borrowed])
        return response
    
    export_to_csv.short_description = "Export selected Loans to CSV"