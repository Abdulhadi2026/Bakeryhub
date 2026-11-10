from django.urls import path

from . import views

urlpatterns = [
    path('', views.sales_list, name='sales_list'),
    path('new/', views.pos_sale, name='pos_sale'),
    path('<int:pk>/', views.sale_detail, name='sale_detail'),
    path('<int:pk>/receipt/', views.receipt, name='receipt'),
]
