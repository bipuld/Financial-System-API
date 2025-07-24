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
from finance.models import Loan


logger = logging.getLogger('django')

class LoanApiView(APIView):
    "Class for Loan Management for the User"
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  
    @swagger_auto_schema(
        operation_description="Creating loan for the user",
        request_body=LoanSerializers,
        responses={
           SUCCESS_RESPONSE_CODE: openapi.Response('Loan Added Successfully.'),
            UNSUCCESS_RESPONSE_CODE: openapi.Response('Bad Request.'),
        }
    )
    def post(self, request):
        "Method to add the Loan"
        try:
            serializers = LoanSerializers(data=request.data)
            if serializers.is_valid():
                    serializers.save(user=request.user)
                    response = {
                        RESPONSE_CODE_KEY: SUCCESS_RESPONSE_CODE,
                        RESPONSE_MESSAGE_KEY: "Loan Added successfully.",
                    }
                    logger.info("Loan Added successfullyfor user: %s", request.user)
                    return Response(response, status=status.HTTP_201_CREATED)
            messages={
                    RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: 'Invalid data.',
                    ERROR_KEY: serializers.errors
                }
            return Response(messages, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error for creating Loan Added successfully: %s", str(e))
            response = {
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "An error occurred while creation of Loan records.",
                ERROR_KEY: str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="Get the current user's Loan Data.",
        manual_parameters=[
            openapi.Parameter(
                'page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'status', openapi.IN_QUERY, description="Filter by Loan status (e.g., 'Active' or 'Paid')", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'loan_name', openapi.IN_QUERY, description="Filter by name of loan (e.g., 'Auto Loan')", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'rem_amnt_gte', openapi.IN_QUERY, description="Provide the amount that is greater than reamining amount eg.50000", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'rem_amnt_lte', openapi.IN_QUERY, description="Provide the amount that is less than reamining amount eg.100000", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'sort', openapi.IN_QUERY, description="Sort results by a field (e.g., 'loan_name' or 'principal_amount' or 'remaining_balance')", type=openapi.TYPE_STRING
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
            loan_name = request.query_params.get('loan_name')
            sort_by = request.query_params.get('sort', None)
            rem_amnt_gte = request.query_params.get('rem_amnt_gte', None)
            rem_amnt_lte = request.query_params.get('rem_amnt_lte', None)
            loan_data = Loan.objects.filter(user=user)
            if status:
                loan_data = loan_data.filter(status=status)
            if loan_name:
                loan_data = loan_data.filter(loan_name__icontains=loan_name)
            if rem_amnt_lte:
                loan_data = loan_data.filter(remaining_balance__lte=rem_amnt_lte)
            if rem_amnt_gte:
                loan_data = loan_data.filter(remaining_balance__gte=rem_amnt_gte)
            if sort_by:
                loan_data = loan_data.order_by(sort_by)

            # Set up pagination
            paginator = PageNumberPagination()
            paginator.page_size = 2  # Items per page
            paginator.page_size_query_param = 'page_size'  # Allows clients to control page size via 'page_size' parameter
            paginator.page_query_param = 'page'  # The parameter name for pagination (defaults to 'page')
            paginator.request = request  # Required for pagination metadata

            # Paginate the query 
            result_page = paginator.paginate_queryset(loan_data, request)
            serializer = LoanSerializers(result_page, many=True)

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
        operation_description="Update the Loan Data and Add the 'loan_id'",
        request_body=LoanSerializers,
        required=['loan_id'],
        responses={
            SUCCESS_RESPONSE_CODE: openapi.Response('Loan Updated Successfully.'),
            UNSUCCESS_RESPONSE_CODE: openapi.Response('Bad Request.'),
            500: openapi.Response('Internal Server Error.'),
        }
    )

    def put(self, request):
        """ Update the Loan Data and Add the 'loan_id' """
        try:
            user=request.user
            loan_data = request.data
            loan_id = loan_data.get('loan_id')
            loan = Loan.objects.filter(user=user, id=loan_id).first()
            if not loan:
                response = {
                    RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: "Loan of this record not found in our records .",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            serializers=LoanSerializers(loan, data=loan_data, partial=True)
            if serializers.is_valid():
                serializers.save()
                response = {
                    RESPONSE_CODE_KEY: SUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: "Loan updated successfully.",
                }
                logger.info("Loan updated successfully for user: %s", request.user)
                return Response(response, status=status.HTTP_200_OK)
            messages={
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: 'Invalid data.',
                ERROR_KEY: serializers.errors
            }
            return Response(messages, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error updating loan records: %s", str(e))
            response = {
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "An error occurred while updating loan records.",
                ERROR_KEY: str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    delete_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'loan_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The ID of the Loan record to be deleted')
        },
        required=['loan_id'],
        operation_description="Deleting Income",
    )

    @swagger_auto_schema(request_body=delete_body) 


    def delete(self,request):
        """ Delete the Loan Data and Add the 'loan_id' """
        try:
            user=request.user
            loan_data = request.data
            loan_id = loan_data.get('loan_id')
            loan = Loan.objects.filter(user=user, id=loan_id).first()
            if not loan:
                response = {
                    RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                    RESPONSE_MESSAGE_KEY: "Loan of this record not found in our records .",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            loan.delete()
            response = {
                RESPONSE_CODE_KEY: SUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "Loan deleted successfully.",
            }
            logger.info("Loan deleted successfully for user: %s", request.user)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error deleting loan records: %s", str(e))
            response = {
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "An error occurred while deleting loan records.",
                ERROR_KEY: str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)