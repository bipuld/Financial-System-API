from django.db import models
from core.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.
class Income(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='incomes')
    source_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField(default=timezone.now)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Received', 'Received'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='Pending')
    notes = models.TextField(blank=True, null=True)
    
    def clean(self):
        "This validation that let the amount to be positive"
        if self.amount < 0:
            raise ValidationError("Amount cannot be negative.")

    class Meta:
        ordering = ['-date_received', '-amount']
        verbose_name = "Income Record"
        verbose_name_plural = "Income Records"
        db_table = "income_table"

    def __str__(self):
        return f"{self.source_name} - {self.amount} ({self.status})"



class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(default=timezone.now)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)

    def clean(self):
        "Validation Amount to be positive"
        if self.amount < 0:
            raise ValidationError("Amount cannot be negative.")

    class Meta:
        ordering = ['-due_date', '-amount']
        verbose_name = "Expense Record"
        verbose_name_plural = "Expense Records"
        db_table = "expense_table"

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.status})"
    
    