# report_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router and register our viewset with it.
router = DefaultRouter()
# router.register(r'report_definitions', ReportDefinitionViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # path('', include(router.urls)),
    # path('execute-report/<int:report_id>/', ExecuteReportView.as_view(), name='execute-report'),
    # path('monthly-sales/', MonthlySalesCountView.as_view(), name='monthly_sales_count'),
    path('report/<str:query_name>/', reports.as_view(), name='Reports_Generation' )

]

