from django.urls import path

from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('movement/', views.stock_movement_form, name='stock_movement_form'),
    path('movement/<int:pk>/delete/', views.stock_movement_delete, name='stock_movement_delete'),
]
