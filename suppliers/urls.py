from django.urls import path

from . import views

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('new/', views.supplier_form, name='supplier_new'),
    path('<int:pk>/edit/', views.supplier_form, name='supplier_edit'),
    path('<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
]
