from django.urls import path

from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('new/', views.order_form, name='order_new'),
    path('<int:pk>/edit/', views.order_form, name='order_edit'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
]
