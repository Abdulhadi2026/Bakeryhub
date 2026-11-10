import json
from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import render

from customers.models import Customer
from employees.models import Employee
from expenses.models import Expense
from inventory.models import Inventory, StockMovement
from orders.models import Order
from products.models import Product
from sales.models import Sale, SaleItem
from suppliers.models import Supplier


@login_required
def dashboard_view(request):
    total_revenue = Sale.objects.filter(status='completed').aggregate(total=Sum('total_amount'))['total'] or 0
    total_sales = Sale.objects.filter(status='completed').count()
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()
    total_employees = Employee.objects.count()
    total_suppliers = Supplier.objects.count()
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    available_stock = Inventory.objects.aggregate(total=Sum('quantity'))['total'] or 0
    low_stock = Product.objects.filter(quantity__lte=F('min_stock'))[:5]
    recent_transactions = Sale.objects.select_related('customer').order_by('-created_at')[:6]
    recent_orders = Order.objects.order_by('-created_at')[:5]
    best_products = (
        SaleItem.objects.values('product__name')
        .annotate(total_quantity=Sum('quantity'), total_revenue=Sum('subtotal'))
        .order_by('-total_quantity')[:5]
    )

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    monthly_sales = []
    current_year = date.today().year
    for month in range(1, 7):
        info = Sale.objects.filter(created_at__month=month, created_at__year=current_year).aggregate(total=Sum('total_amount'))
        monthly_sales.append({
            'label': month_names[month - 1],
            'value': float(info['total'] or 0),
        })
    chart_data = json.dumps(monthly_sales)

    top_customers = Sale.objects.values('customer__name').annotate(total=Sum('total_amount')).order_by('-total')[:5]
    recent_movements = StockMovement.objects.select_related('product').order_by('-created_at')[:6]

    context = {
        'total_revenue': total_revenue,
        'total_sales': total_sales,
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_employees': total_employees,
        'total_suppliers': total_suppliers,
        'total_expenses': total_expenses,
        'available_stock': available_stock,
        'low_stock': low_stock,
        'recent_transactions': recent_transactions,
        'recent_orders': recent_orders,
        'best_products': best_products,
        'monthly_sales': monthly_sales,
        'chart_data': chart_data,
        'top_customers': top_customers,
        'recent_movements': recent_movements,
    }
    return render(request, 'dashboard.html', context)
