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
from finance.models import Income


logger = logging.getLogger('django')
class IncomeManagment(APIView):
    "View for Income Management"
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  
    @swagger_auto_schema(
        operation_description="Creating Income",
        request_body=IncomeSerizlier,
        responses={
           SUCCESS_RESPONSE_CODE: openapi.Response('Income Created Successfully.'),
            UNSUCCESS_RESPONSE_CODE: openapi.Response('Bad Request.'),
        }
    )
    def post(self, request):
        """Create the current user's income put the current user access token in headers as Bearer token fot authoriazation and pass the income data in the request body"""
        try:
            user=request.user
            income_data = request.data
            print(income_data)
            exist_income = Income.objects.filter(user=user, source_name=income_data['source_name'], amount=income_data['amount'], date_received=income_data['date_received']).exists()
            if exist_income:
                response = {
                    RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: "Income already exists.",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            serializers=IncomeSerizlier(data=income_data)
            if serializers.is_valid():
                serializers.save(user=user)
                response = {
                    RESPONSE_CODE_KEY: SUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: "Income created successfully.",
                }
                logger.info("Income created successfully for user: %s", request.user)
                return Response(response, status=status.HTTP_201_CREATED)
            messages={
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: 'Invalid data.',
                ERROR_KEY: serializers.errors
            }
            return Response(messages, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error for creating income records: %s", str(e))
            response = {
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "An error occurred while creation of  income records.",
                ERROR_KEY: str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Get the current user's income.",
        manual_parameters=[
            openapi.Parameter(
                'page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'status', openapi.IN_QUERY, description="Filter by income status (e.g., 'Pending' or 'Received')", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'date_received', openapi.IN_QUERY, description="Filter by date received (YYYY-MM-DD) (e.g., '2024-10-15')", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'source_name', openapi.IN_QUERY, description="Filter by source of income (e.g., 'Salary')", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'sort', openapi.IN_QUERY, description="Sort results by a field (e.g., 'amount' or '-date_received')", type=openapi.TYPE_STRING
            ),
        ],
        responses={
            SUCCESS_RESPONSE_CODE: openapi.Response('Income retrieved successfully.'),
            UNSUCCESS_RESPONSE_CODE: openapi.Response('Bad Request.'),
            500: openapi.Response('Internal Server Error.'),
        }
    )
    def get(self, request):
        """
        Get the current user's income. Provide current user access token in headers as - Bearer token.
        """
        try:
            user = request.user
            status = request.query_params.get('status')
            date_received = request.query_params.get('date_received')
            source_name = request.query_params.get('source_name')
            sort_by = request.query_params.get('sort', None)
            incomes = Income.objects.filter(user=user)
            if status:
                incomes = incomes.filter(status=status)
            if date_received:
                incomes = incomes.filter(date_received=date_received)
            if source_name:
                incomes = incomes.filter(source_name__icontains=source_name)
            if sort_by:
                incomes = incomes.order_by(sort_by)

            # Set up pagination
            paginator = PageNumberPagination()
            paginator.page_size = 2  # Items per page
            paginator.page_size_query_param = 'page_size'  # Allows clients to control page size via 'page_size' parameter
            paginator.page_query_param = 'page'  # The parameter name for pagination (defaults to 'page')
            paginator.request = request 

            # Paginate the query 
            result_page = paginator.paginate_queryset(incomes, request)
            serializer = IncomeSerizlier(result_page, many=True)

            # Return paginated response with metadata
            return paginator.get_paginated_response({
                RESPONSE_CODE_KEY: SUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: 'Income retrieved successfully.',
                RESULT_DATA: serializer.data
            })

        except Exception as e:
            logger.error("Error retrieving income records: %s", str(e))
            return Response({
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: 'An error occurred while retrieving income records.',
                ERROR_KEY: str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    @swagger_auto_schema(
        operation_description="Updating Income and Add the 'income_id' in the request body",
        request_body=IncomeSerizlier,
        required=['income_id'],
        responses={
            SUCCESS_RESPONSE_CODE: openapi.Response('Income updated successfully.'),
            UNSUCCESS_RESPONSE_CODE: openapi.Response('Bad Request.'),
        }
    )

    def put(self, request):
        """Update the current user's income put the current user access token in headers as Bearer token and pass the income_id in the request body"""
        try:
            user=request.user
            income_data = request.data
            income_id = income_data.get('income_id')
            income = Income.objects.filter(user=user, id=income_id).first()
            if not income:
                response = {
                    RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: "Income not found.",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            serializers=IncomeSerizlier(income, data=income_data, partial=True)
            if serializers.is_valid():
                serializers.save()
                response = {
                    RESPONSE_CODE_KEY: SUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: "Income updated successfully.",
                }
                logger.info("Income updated successfully for user: %s", request.user)
                return Response(response, status=status.HTTP_200_OK)
            messages={
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: 'Invalid data.',
                ERROR_KEY: serializers.errors
            }
            return Response(messages, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error updating income records: %s", str(e))
            response = {
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "An error occurred while updating income records.",
                ERROR_KEY: str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    delete_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'income_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The ID of the income record to be deleted')
        },
        required=['income_id'],
        operation_description="Deleting Income",
    )

    @swagger_auto_schema(request_body=delete_body) 

    def delete(self, request):
        """Delete the current user's income put the current user access token in headers as Bearer token and pass the income_id in the request body"""
        try:
            user=request.user
            income_data = request.data
            income_id = income_data.get('income_id')
            income = Income.objects.filter(user=user, id=income_id).first()
            if not income:
                response = {
                    RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: "Income not found.",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            income.delete()
            response = {
                RESPONSE_CODE_KEY: SUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "Income deleted successfully.",
            }
            logger.info("Income deleted successfully for user: %s", request.user)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error deleting income records: %s", str(e))
            response = {
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "An error occurred while deleting income records.",
                ERROR_KEY: str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)