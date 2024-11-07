# report_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router and register our viewset with it.
router = DefaultRouter()

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # path('', include(router.urls)),
    # path('execute-report/<int:report_id>/', ExecuteReportView.as_view(), name='execute-report'),
    # path('monthly-sales/', MonthlySalesCountView.as_view(), name='monthly_sales_count'),
    path('report/<str:query_name>/', reports.as_view(), name='Reports_Generation' ),
    path('tables/', DatabaseView.as_view(), name='return-tables'),  #List down the tables
    path('tables/<str:table_name>/columns/', DatabaseView.as_view(), name='return-tables-columns'),   #List down the selected table's columns 
    path('execute_query/', ExecuteQueryView.as_view(), name='execute-query'),
    path('save_query/', ReportDefinitionView.as_view(), name='save-custom-query'),

 ]
