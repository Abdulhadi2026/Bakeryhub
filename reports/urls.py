from django.urls import path

from . import views

urlpatterns = [
    path('', views.report_dashboard, name='report_dashboard'),
    path('sales/', views.sales_report, name='sales_report'),
    path('inventory/', views.inventory_report, name='inventory_report'),
    path('expenses/', views.expense_report, name='expense_report'),
    path('profit/', views.profit_report, name='profit_report'),
    path('export/', views.export_csv, name='export_csv'),
]
