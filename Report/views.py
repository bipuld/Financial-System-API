import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from FinanceFlow.global_msg import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from finance.serializers.loan_serializers   import *
from rest_framework.pagination import PageNumberPagination
from finance.models import *
from django.db.models import Sum


logger = logging.getLogger('django')


class SummaryReport(APIView):
    """This class is used to generate summary report"""
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    @swagger_auto_schema(
        operation_summary="Get summary report",
        operation_description="Fetch summary of total income, expenses, and active loans within a specified date range.",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Start date (YYYY-MM-DD)', required=False),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='End date (YYYY-MM-DD)', required=False)

        ],
        responses={
            SUCCESS_RESPONSE_CODE: openapi.Response('Summary Report', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'total_income': openapi.Schema(type=openapi.TYPE_NUMBER, format='decimal', description='Total income within the date range'),
                    'total_expenses': openapi.Schema(type=openapi.TYPE_NUMBER, format='decimal', description='Total expenses within the date range'),
                    'active_loans': openapi.Schema(type=openapi.TYPE_INTEGER, description='Count of active loans'),
                }
            )),
            UNSUCCESS_RESPONSE_CODE: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Internal Server Error'
        }
        )
    def get(self, request):
            user=request.user
            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)
            incomes = Income.objects.filter(user=user)
            print(incomes,"incomes")
            if start_date and end_date:
                incomes = incomes.filter(date_received__range=[start_date, end_date])  
            # type casting 
            income_sum = incomes.aggregate(total=Sum('amount'))
            # print(income_sum,"income_sum")
            total_income = income_sum['total'] if income_sum['total'] else 0.0
            # print(total_income,"total_income")
            expenses = Expense.objects.filter(user=user)
            if start_date and end_date:
                expenses = expenses.filter(due_date__range=[start_date, end_date])
            expenses_sum = expenses.aggregate(total=Sum('amount'))
            # print(expenses_sum,"expenses")
            total_expenses = expenses_sum['total'] if expenses_sum['total'] else 0.0
            # print(total_expenses,"total_expenses")

            # Count active loans
            active_loans_count = Loan.objects.filter(status='Active').count()
            print(active_loans_count,"active_loans_count")
            # Return response
            return Response({
                'total_income': total_income,
                'total_expenses': total_expenses,
                'active_loans': active_loans_count
            })
    
