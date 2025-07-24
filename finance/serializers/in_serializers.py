from rest_framework import serializers
from finance.models import Income

class IncomeSerizlier(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id','source_name','amount','date_received','status','notes']

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative.")
        return value
    
    