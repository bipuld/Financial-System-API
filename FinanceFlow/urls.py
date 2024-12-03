from django.contrib import admin
from django.urls import path,re_path,include
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from Report import views as report_views


schema_view = get_schema_view(
    openapi.Info(
        title="FinanceFlow API",
        default_version='v1',
        description="API documentation for FinanceFlow",
        contact=openapi.Contact(email="bipuldawadi14@gmail.com"),
        license=openapi.License(name="XYZ License"),
    ),
    public=True,
    # url='https://bipuld.pythonanywhere.com',
    permission_classes=(AllowAny,), 
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('core.urls')), 
    path('api/finance/', include('finance.urls')),
    path('api/summary/', include('Report.urls')),
    # path('chart/',report_views.TrendViews, name='income_expenses'),
    path('', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
]


