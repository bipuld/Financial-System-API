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
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.template import TemplateDoesNotExist
from django.shortcuts import render
logger = logging.getLogger('django')
import json
from decimal import Decimal

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
            loan=[]
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
        
            active_loans = Loan.objects.filter(status='Active')
            print("Loan are ",active_loans)
            for i in active_loans:
                data = {
                    "loan_name":i.loan_name,
                    "loan_amount":i.principal_amount,
                    "interest_rate":i.interest_rate,
                    "loan_period":i.tenure_months,
                    "emi":i.monthly_installment,
                    "Remaining_amount":i.principal_amount,
                }
                loan.append(data)
            # Return response
            return Response({
                'total_income': total_income,
                'total_expenses': total_expenses,
                'active_loans': active_loans.count(),
                "loan":loan
            })
    
class IncomeExpenseTrendView(APIView):
    """This class is used to generate income and expense trend report"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_summary="Get income and expense trend report",
        operation_description="Fetch income and expense trend report within a specified date range.",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Start date (YYYY-MM-DD)', required=False),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='End date (YYYY-MM-DD)', required=False),
            openapi.Parameter('Accept', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Response format', enum=['application/json', 'text/html'], default='application/json')  
        ],
        responses={
            200: openapi.Response('Trend Report', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='Income and expense trend report within the date range with daily breakdown',
                properties={
                    'start_date': openapi.Schema(type=openapi.TYPE_STRING, description="Start date"),
                    'end_date': openapi.Schema(type=openapi.TYPE_STRING, description="End date"),
                    'trends': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)),
                }
            )),
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Internal Server Error',
        }
    )
    def get(self, request):
        user = request.user
        report = []
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        print(start_date,"start_date")
        print(end_date,"end_date")
        try:
            if start_date and end_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                if start_date > end_date:
                    return Response({"error": "start_date cannot be greater than end_date."}, status=400)
            else:
                end_date = now().date()
                start_date = end_date - timedelta(days=30)  # default 30 days
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD (e.g., 2023-05-02)"}, status=400)
        current_date = start_date
        while current_date <= end_date:
            income_sum = (Income.objects.filter(
                user=user,
                date_received=current_date
            ).aggregate(total=Sum('amount'))['total'] or 0.0)

            expense_sum = (Expense.objects.filter(
                user=user,
                due_date=current_date
            ).aggregate(total=Sum('amount'))['total'] or 0.0)

            report.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "income": income_sum,
                "expense": expense_sum
            })

            current_date += timedelta(days=1)
        print(report,"report")
        if 'text/html' in request.headers.get('Accept', ''):
            for item in report:
                item['income'] = float(item['income'])
                item['expense'] = float(item['expense'])

            return self.render_trend_view(request, start_date, end_date, report)

        data = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "trends": report,
        }
        return Response(data, status=200)

    def render_trend_view(self, request, start_date, end_date, report):
        try:
            dates = [entry['date'] for entry in report]
            incomes = [entry['income'] for entry in report]
            expenses = [entry['expense'] for entry in report]
            # print(incomes,"incomes")
            # print(expenses,"expenses")
            # print(dates,"dates")
            return render(request, 'chart.html', {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "trends": report,
                "dates": dates,
                "incomes": incomes,
                "expenses": expenses
            })
        except TemplateDoesNotExist:
            return Response({"error": "Template 'chart.html' not found"}, status=404)
