from rest_framework import serializers
from finance.models import Expense


class ExpensesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id','category','amount','due_date','status','notes']

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative.")
        return value
    
    