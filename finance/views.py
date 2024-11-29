import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from FinanceFlow.global_msg import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate

logger = logging.getLogger('django')

class IncomeManagment(APIView):
    "View for Income Management"
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user",
        # request_body=RegisterSerializer,
        responses={
            201: openapi.Response('User registered successfully.'),
            400: openapi.Response('Bad Request.'),
        }
    )
    def get(self, request):
        try:
            income_data = [
                {"id": 1, "source_name": "Salary", "amount": 5000, "status": "Received"},
                {"id": 2, "source_name": "Freelance", "amount": 2000, "status": "Pending"},
            ]

            response = {
                RESPONSE_CODE_KEY: SUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "Income records retrieved successfully.",
                RESULT_DATA: income_data,
            }
            logger.info("Income records retrieved successfully for user: %s", request.user)
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("Error retrieving income records: %s", str(e))
            response = {
                RESPONSE_CODE_KEY: UNSUCCESS_RESPONSE_CODE,
                RESPONSE_MESSAGE_KEY: "An error occurred while retrieving income records.",
                ERROR_KEY: str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
