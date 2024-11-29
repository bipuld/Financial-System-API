import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from django.contrib.auth import logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate

logger = logging.getLogger('django')
class RegisterView(APIView):
    "view for user registration"
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response('User registered successfully.'),
            400: openapi.Response('Bad Request.'),
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    "API endpoint for user login. This allow us to Login the user."    
    permission_classes = [AllowAny]


    @swagger_auto_schema(
        operation_description="Login a user and get JWT tokens",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response('Login successful, returns access and refresh tokens.'),
            400: openapi.Response('Bad Request.'),
            401: openapi.Response('Invalid credentials.'),
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    "View for getting and updating user profile"
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  

    @swagger_auto_schema(
        operation_description="Get user profile",
        responses={
            200: ProfileSerializer,
            401: openapi.Response('Unauthorized'),
        }
    )
    def get(self, request):
        """Get the current user's profile and put the current user access token in headers as Bearer token"""
        
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update user profile",
        request_body=ProfileSerializer,
        responses={
            200: openapi.Response('Profile updated successfully.'),
            400: openapi.Response('Bad Request.'),
            401: openapi.Response('Unauthorized.'),
        }
    )
    def put(self, request):
        """Update the current user's profile put the current user access token in headers as Bearer token"""
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    """
    API endpoint for user logout. Put the current user access token in headers as Bearer token and This logs out the user".
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # JWT Authentication to the view

    @swagger_auto_schema(
        operation_description="Log out the user and revoke refresh token",
        responses={
            200: openapi.Response('User logged out successfully.'),
            400: openapi.Response('Bad Request.'),
            401: openapi.Response('Unauthorized.'),
        },
        security=[{'Bearer': []}]  # Swagger documentation for the Bearer token
    )
    def post(self, request):
        """Log out the user and revoke refresh token"""
        try:
          
            refresh_token = RefreshToken.for_user(request.user)
            refresh_token.blacklist()
            logout(request)
            return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
