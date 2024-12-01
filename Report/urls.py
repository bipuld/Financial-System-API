from django.urls import path,re_path,include
from .import views

urlpatterns = [
    path('report/', views.SummaryReport.as_view(), name='summary'),
    path('income-expenses-trends/', views.IncomeExpenseTrendView.as_view(), name='income_expenses_trends'),
    # path('chart/',views.TrendViews, name='income_expenses'),
]