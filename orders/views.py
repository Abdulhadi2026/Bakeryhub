from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from customers.models import Customer
from inventory.models import Inventory, StockMovement
from products.models import Product
from .forms import OrderForm
from .models import Order, OrderItem


def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def cart_view(request):
    cart = _get_cart(request)
    items = []
    total = Decimal('0')

    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
        except (TypeError, ValueError, Product.DoesNotExist):
            continue

        quantity = max(1, int(item_data.get('quantity', 1)))
        subtotal = product.selling_price * quantity
        total += subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'orders/cart.html', {'items': items, 'total': total})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = max(1, int(request.POST.get('quantity', 1)))

    if quantity > product.quantity:
        messages.error(request, f'Only {product.quantity} units of {product.name} are available.')
        return redirect('product_list')

    cart = _get_cart(request)
    key = str(product_id)
    current_quantity = int(cart.get(key, {}).get('quantity', 0))
    cart[key] = {'quantity': current_quantity + quantity}
    _save_cart(request, cart)

    messages.success(request, f'{product.name} added to cart.')
    return redirect('product_list')


def update_cart_item(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = _get_cart(request)
    key = str(product_id)

    if request.method == 'POST':
        quantity = max(1, int(request.POST.get('quantity', 1)))
        if quantity > product.quantity:
            messages.error(request, f'Only {product.quantity} units of {product.name} are available.')
        else:
            cart[key] = {'quantity': quantity}
            _save_cart(request, cart)
            messages.success(request, f'{product.name} updated in the cart.')

    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = _get_cart(request)
    cart.pop(str(product_id), None)
    _save_cart(request, cart)
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


def _resolve_customer_for_checkout(request):
    customer_id = request.POST.get('customer')
    if customer_id:
        return get_object_or_404(Customer, pk=customer_id)

    name = (request.POST.get('customer_name') or '').strip()
    phone = (request.POST.get('customer_phone') or '').strip()
    email = (request.POST.get('customer_email') or '').strip()
    address = (request.POST.get('customer_address') or '').strip()

    if not name or not phone:
        raise ValueError('Customer name and phone number are required.')

    customer, _ = Customer.objects.get_or_create(
        phone=phone,
        defaults={'name': name, 'email': email or None, 'address': address},
    )
    if customer.name != name:
        customer.name = name
    if email and not customer.email:
        customer.email = email
    if address and not customer.address:
        customer.address = address
    customer.save()
    return customer


def checkout(request):
    cart = _get_cart(request)
    if not cart:
        messages.info(request, 'Your cart is empty.')
        return redirect('product_list')

    items = []
    total = Decimal('0')
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
        except (TypeError, ValueError, Product.DoesNotExist):
            continue

        quantity = max(1, int(item_data.get('quantity', 1)))
        if quantity > product.quantity:
            messages.error(request, f'{product.name} no longer has enough stock for your order.')
            return redirect('cart')

        subtotal = product.selling_price * quantity
        total += subtotal
        items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    if request.method == 'POST':
        try:
            customer = _resolve_customer_for_checkout(request)
        except ValueError as exc:
            messages.error(request, str(exc))
            return redirect('checkout')

        delivery_date = request.POST.get('delivery_date') or None
        notes = request.POST.get('notes', '').strip()
        payment_method = request.POST.get('payment_method', 'cash')

        if notes:
            notes = f'{notes} | Payment: {payment_method}'
        else:
            notes = f'Payment: {payment_method}'

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    customer=customer,
                    delivery_date=delivery_date,
                    notes=notes,
                    total_amount=Decimal('0'),
                    status='pending',
                )

                for item in items:
                    product = item['product']
                    quantity = item['quantity']
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=product.selling_price,
                    )

                    inventory, _ = Inventory.objects.get_or_create(product=product)
                    inventory.quantity = product.quantity
                    inventory.min_stock = product.min_stock
                    inventory.save()

                    StockMovement.objects.create(
                        product=product,
                        movement_type='out',
                        quantity=quantity,
                        reference=order.order_number,
                        notes=f'Order placed for {customer.name}',
                    )

                order.total_amount = total
                order.save()

        except Exception:
            messages.error(request, 'The order could not be placed. Please try again.')
            return redirect('cart')

        request.session['cart'] = {}
        messages.success(request, f'Order {order.order_number} placed successfully.')
        if request.user.is_authenticated:
            return redirect('order_list')
        return redirect('product_list')

    customers = Customer.objects.order_by('name')
    return render(request, 'orders/checkout.html', {'items': items, 'total': total, 'customers': customers})


@login_required
def order_list(request):
    query = request.GET.get('q', '').strip()
    orders = Order.objects.select_related('customer').order_by('-created_at')
    if query:
        orders = orders.filter(Q(order_number__icontains=query) | Q(customer__name__icontains=query) | Q(status__icontains=query))
    return render(request, 'orders/order_list.html', {'orders': orders, 'query': query})


@login_required
def order_form(request, pk=None):
    order = get_object_or_404(Order, pk=pk) if pk else None
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            saved_order = form.save()
            messages.success(request, f"Order '{saved_order.order_number}' saved successfully.")
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form, 'order': order})


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    messages.success(request, 'Order deleted successfully.')
    return redirect('order_list')
