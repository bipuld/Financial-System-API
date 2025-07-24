from rest_framework import serializers
from finance.models import Loan


class LoanSerializers(serializers.ModelSerializer):
    # Custom formatted fields for display purposes
    formatted_monthly_installment = serializers.SerializerMethodField()
    formatted_remaining_balance = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['id', 'loan_name', 'principal_amount', 'interest_rate', 'tenure_months', 'monthly_installment', 'remaining_balance', 'status', 'notes', 'formatted_monthly_installment', 'formatted_remaining_balance']
        read_only_fields = ('monthly_installment', 'remaining_balance', 'formatted_monthly_installment', 'formatted_remaining_balance')

     # To format monthly_installment
    def get_formatted_monthly_installment(self, obj):
        return f"Rs {obj.monthly_installment:,.2f}"

    # To format remaining_balance
    def get_formatted_remaining_balance(self, obj):
        return f"Rs {obj.remaining_balance:,.2f}"

    # Validation for interest_rate
    def validate_interest_rate(self, value):
        if not (0 <= value <= 100):
            raise serializers.ValidationError("Interest rate must be between 0 and 100.")
        return value

    # Validation for principal_amount to can poisitive
    def validate_principal_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Principal amount must be greater than zero.")
        return value

    # Custom validation for tenure_months to ensure it's positive
    def validate_tenure_months(self, value):
        if value <= 0:
            raise serializers.ValidationError("Tenure months must be greater than zero.")
        return value