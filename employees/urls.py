from django.urls import path

from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('new/', views.employee_form, name='employee_new'),
    path('<int:pk>/edit/', views.employee_form, name='employee_edit'),
    path('<int:pk>/delete/', views.employee_delete, name='employee_delete'),
]
