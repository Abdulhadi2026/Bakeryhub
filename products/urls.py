from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('new/', views.product_form, name='product_new'),
    path('<int:pk>/edit/', views.product_form, name='product_edit'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_form, name='category_new'),
    path('categories/<int:pk>/edit/', views.category_form, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
