from django.urls import path
from .views import *

urlpatterns = [
    path('income/', IncomeManagment.as_view(), name='income'),
    path('expense/', ExpensesView.as_view(), name='expense'),
    path('loan/', LoanApiView.as_view(), name='loan'),
]


