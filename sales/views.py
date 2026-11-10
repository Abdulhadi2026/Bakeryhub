from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from customers.models import Customer
from inventory.models import Inventory, StockMovement
from products.models import Product

from .models import Payment, Sale, SaleItem


@login_required
def sales_list(request):
    sales = Sale.objects.select_related('customer').order_by('-created_at')
    return render(request, 'sales/sales_list.html', {'sales': sales})


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sale_detail.html', {'sale': sale})


@login_required
def receipt(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/receipt.html', {'sale': sale})


@login_required
def pos_sale(request):
    products = Product.objects.filter(is_active=True).order_by('name')
    customers = Customer.objects.order_by('name')
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')
        customer_id = request.POST.get('customer')
        discount = Decimal(request.POST.get('discount', '0') or '0')
        payment_method = request.POST.get('payment_method', 'cash')

        if not product_ids:
            messages.error(request, 'Please add at least one product to the sale.')
            return render(request, 'sales/pos.html', {'products': products, 'customers': customers})

        try:
            with transaction.atomic():
                sale = Sale.objects.create(
                    customer=Customer.objects.filter(pk=customer_id).first() if customer_id else None,
                    discount=discount,
                    payment_method=payment_method,
                    status='completed',
                )
                total = Decimal('0')
                for index, product_id in enumerate(product_ids):
                    if not product_id:
                        continue
                    product = get_object_or_404(Product, pk=product_id)
                    quantity = int(quantities[index]) if index < len(quantities) else 1
                    if quantity <= 0:
                        continue
                    if product.quantity < quantity:
                        raise ValueError(f'Not enough stock for {product.name}.')
                    subtotal = product.selling_price * quantity
                    total += subtotal
                    SaleItem.objects.create(
                        sale=sale,
                        product=product,
                        quantity=quantity,
                        unit_price=product.selling_price,
                        subtotal=subtotal,
                    )
                    product.quantity -= quantity
                    product.save()
                    inventory, _ = Inventory.objects.get_or_create(product=product)
                    inventory.quantity = product.quantity
                    inventory.save()
                    StockMovement.objects.create(
                        product=product,
                        movement_type='out',
                        quantity=quantity,
                        reference=sale.sale_number,
                        notes='Sale transaction',
                    )
                sale.total_amount = total - discount
                sale.save()
                Payment.objects.create(sale=sale, amount=sale.total_amount, method=payment_method)
                messages.success(request, f'Sale {sale.sale_number} completed successfully.')
                return redirect('receipt', pk=sale.pk)
        except ValueError as exc:
            messages.error(request, str(exc))

    return render(request, 'sales/pos.html', {'products': products, 'customers': customers})
