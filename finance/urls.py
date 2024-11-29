from django.urls import path
from .views import IncomeManagment

urlpatterns = [
    path('income/', IncomeManagment.as_view(), name='income'),
]


