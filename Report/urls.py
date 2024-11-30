from django.urls import path,re_path,include
from .import views

urlpatterns = [
    path('report/', views.SummaryReport.as_view(), name='summary'),
]