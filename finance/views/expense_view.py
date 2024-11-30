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
from finance.serializers import *
from rest_framework.pagination import PageNumberPagination
from finance.models import Expense

logger = logging.getLogger('django')

class ExpensesView(APIView):
    "Class for Expenses Management"
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  
    @swagger_auto_schema(
        operation_description="Expense Creation",
        request_body=ExpensesSerializers,
        responses={
           SUCCESS_RESPONSE_CODE: openapi.Response('Expenses Creation Successfully.'),
            UNSUCCESS_RESPONSE_CODE: openapi.Response('Bad Request.'),
        }
        
    )
    def post(self,request):
        "Method for Expense Creation"
        try:
            user=request.user
            expenses_data = request.data
            serializers=ExpensesSerializers(data=expenses_data)
            if serializers.is_valid():
                serializers.save(user=user)
                response = {
                    RESPONSE_CODE_KEY: SUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: "Expenses Added successfully in your account.",
                }
                logger.info("Expenses created successfully for user: %s", request.user)
                return Response(response, status=status.HTTP_201_CREATED)
            messages={
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: 'Invalid data.',
                ERROR_KEY: serializers.errors
            }
            return Response(messages, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error retrieving Expenses records: %s", str(e))
            response = {
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "An error occurred while Expenses  records.",
                ERROR_KEY: str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @swagger_auto_schema(
        operation_description="Get the current user's Expenses.",
        manual_parameters=[
            openapi.Parameter(
                'page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'status', openapi.IN_QUERY, description="Filter by Expenses status (e.g., 'Pending' or 'Paid')", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'due_date', openapi.IN_QUERY, description="Filter by Due date (YYYY-MM-DD) (e.g., '2024-10-15')", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'category', openapi.IN_QUERY, description="Filter by category of expenses (e.g., 'Bill')", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'sort', openapi.IN_QUERY, description="Sort results by a field (e.g., 'amount' or '-due_date')", type=openapi.TYPE_STRING
            ),
        ],
        responses={
            SUCCESS_RESPONSE_CODE: openapi.Response('Expenses retrieved successfully.'),
            UNSUCCESS_RESPONSE_CODE: openapi.Response('Bad Request.'),
            500: openapi.Response('Internal Server Error.'),
        }
    )
    def get(self, request):
        """
        Current user's Expenses. Provide current user access token in headers as - Bearer token.
        """
        try:
            user = request.user
            status = request.query_params.get('status')
            due_date = request.query_params.get('due_date')
            category = request.query_params.get('category')
            sort_by = request.query_params.get('sort', None)
            expense = Expense.objects.filter(user=user)
            if status:
                expense = expense.filter(status=status)
            if due_date:
                expense = expense.filter(due_date=due_date)
            if category:
                expense = expense.filter(category__icontains=category)
            if sort_by:
                expense = expense.order_by(sort_by)

            # Set up pagination
            paginator = PageNumberPagination()
            paginator.page_size = 2  # Items per page
            paginator.page_size_query_param = 'page_size'  # clients to control page size via 'page_size' parameter
            paginator.page_query_param = 'page'  # The parameter name for pagination (defaults to 'page')
            paginator.request = request  # Required for pagination metadata

            # Paginate the query 
            result_page = paginator.paginate_queryset(expense, request)
            serializer = ExpensesSerializers(result_page, many=True)

            # Return paginated response with metadata
            return paginator.get_paginated_response({
                RESPONSE_CODE_KEY: SUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: 'Expenses retrieved successfully.',
                RESULT_DATA: serializer.data
            })

        except Exception as e:
            logger.error("Error retrieving Expenses records: %s", str(e))
            return Response({
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: 'An error occurred while retrieving Expenses records.',
                ERROR_KEY: str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    @swagger_auto_schema(
        operation_description="Updating Expenses and Add the 'expense_id' in the request body",
        request_body=ExpensesSerializers,
        required=['expense_id'],
        responses={
            SUCCESS_RESPONSE_CODE: openapi.Response('Expense updated successfully.'),
            UNSUCCESS_RESPONSE_CODE: openapi.Response('Bad Request.'),
        }
    )

    def put(self, request):
        """Update the current user's Expense put the current user access token in headers as Bearer token and pass the expense_id in the request body"""
        try:
            user=request.user
            expense_data = request.data
            expense_id = expense_data.get('expense_id')
            expense = Expense.objects.filter(user=user, id=expense_id).first()
            if not expense:
                response = {
                    RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: "Expenses not found.",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            serializers=ExpensesSerializers(expense, data=expense_data, partial=True)
            if serializers.is_valid():
                serializers.save()
                response = {
                    RESPONSE_CODE_KEY: SUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: "Expense updated successfully.",
                }
                logger.info("Expenses updated successfully for user: %s", request.user)
                return Response(response, status=status.HTTP_200_OK)
            messages={
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: 'Invalid data.',
                ERROR_KEY: serializers.errors
            }
            return Response(messages, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error updating Expense records: %s", str(e))
            response = {
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "An error occurred while updating Expenses records.",
                ERROR_KEY: str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    delete_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'expense_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The ID of the Expenses record to be deleted')
        },
        required=['Expense'],
        operation_description="Deleting expense",
    )

    @swagger_auto_schema(request_body=delete_body) 

    def delete(self, request):
        """Delete the current user's Expenses put the current user access token in headers as Bearer token and pass the expense in the request body"""
        try:
            user=request.user
            expense_data = request.data
            expense_id = expense_data.get('expense_id')
            expense = Expense.objects.filter(user=user, id=expense_id).first()
            if not expense:
                response = {
                    RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: "Expenses not found.",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            expense.delete()
            response = {
                RESPONSE_CODE_KEY: SUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "Expense deleted successfully.",
            }
            logger.info("Expenses deleted successfully for user: %s", request.user)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error deleting Expenses records: %s", str(e))
            response = {
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "An error occurred while deleting Expenses records.",
                ERROR_KEY: str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)