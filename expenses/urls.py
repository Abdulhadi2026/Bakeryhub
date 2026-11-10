from django.urls import path

from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('new/', views.expense_form, name='expense_new'),
    path('<int:pk>/edit/', views.expense_form, name='expense_edit'),
    path('<int:pk>/delete/', views.expense_delete, name='expense_delete'),
]
