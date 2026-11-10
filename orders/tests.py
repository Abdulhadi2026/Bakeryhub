from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from orders.models import Order
from products.models import Category, Product

User = get_user_model()


class CartCheckoutFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='staff', password='pass123')
        self.customer = Customer.objects.create(name='Jane Doe', phone='08012345678', address='Lagos')
        self.category = Category.objects.create(name='Bakery')
        self.product = Product.objects.create(
            category=self.category,
            name='Bread Loaf',
            description='Fresh bread',
            sku='BREAD-001',
            purchase_price=Decimal('200.00'),
            selling_price=Decimal('500.00'),
            quantity=10,
            min_stock=2,
        )

    def test_customer_cart_checkout_creates_order_and_updates_stock(self):
        self.client.force_login(self.user)

        add_url = reverse('add_to_cart', args=[self.product.pk])
        response = self.client.post(add_url, {'quantity': 2})
        self.assertEqual(response.status_code, 302)

        cart = self.client.session.get('cart', {})
        self.assertEqual(cart[str(self.product.pk)]['quantity'], 2)

        checkout_url = reverse('checkout')
        response = self.client.post(
            checkout_url,
            {
                'customer': self.customer.pk,
                'delivery_date': '2026-11-10',
                'notes': 'Please deliver before 5pm.',
                'payment_method': 'cash',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(customer=self.customer).exists())

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 8)

    def test_anonymous_customer_can_order_online(self):
        product_list_url = reverse('product_list')
        response = self.client.get(product_list_url)
        self.assertEqual(response.status_code, 200)

        add_url = reverse('add_to_cart', args=[self.product.pk])
        response = self.client.post(add_url, {'quantity': 2})
        self.assertEqual(response.status_code, 302)

        checkout_url = reverse('checkout')
        response = self.client.post(
            checkout_url,
            {
                'customer_name': 'Home Buyer',
                'customer_phone': '08099998888',
                'customer_email': 'buyer@example.com',
                'customer_address': 'Abuja',
                'delivery_date': '2026-11-15',
                'notes': 'Please ring bell',
                'payment_method': 'mobile',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Customer.objects.filter(phone='08099998888', name='Home Buyer').exists())
        self.assertTrue(Order.objects.filter(customer__phone='08099998888').exists())

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 8)
