import csv
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render

from expenses.models import Expense
from inventory.models import Inventory
from products.models import Product
from sales.models import Sale, SaleItem


@login_required
def report_dashboard(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    sales = Sale.objects.filter(status='completed')
    if start_date:
        sales = sales.filter(created_at__date__gte=start_date)
    if end_date:
        sales = sales.filter(created_at__date__lte=end_date)
    revenue = sales.aggregate(total=Sum('total_amount'))['total'] or 0
    expenses = Expense.objects.all()
    if start_date:
        expenses = expenses.filter(expense_date__gte=start_date)
    if end_date:
        expenses = expenses.filter(expense_date__lte=end_date)
    expense_total = expenses.aggregate(total=Sum('amount'))['total'] or 0
    profit = revenue - expense_total if revenue and expense_total else revenue
    products = Product.objects.filter(quantity__gt=0).order_by('-quantity')[:10]
    stock_summary = Inventory.objects.select_related('product').order_by('product__name')
    return render(request, 'reports/report_dashboard.html', {
        'revenue': revenue,
        'expense_total': expense_total,
        'profit': profit,
        'sales': sales,
        'products': products,
        'stock_summary': stock_summary,
        'start_date': start_date,
        'end_date': end_date,
    })


@login_required
def sales_report(request):
    return report_dashboard(request)


@login_required
def inventory_report(request):
    report_data = Inventory.objects.select_related('product').order_by('product__name')
    return render(request, 'reports/inventory_report.html', {'report_data': report_data})


@login_required
def expense_report(request):
    expenses = Expense.objects.order_by('-expense_date')
    total = expenses.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'reports/expense_report.html', {'expenses': expenses, 'total': total})


@login_required
def profit_report(request):
    sales = Sale.objects.filter(status='completed')
    total_revenue = sales.aggregate(total=Sum('total_amount'))['total'] or 0
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    best_sellers = SaleItem.objects.values('product__name').annotate(quantity=Sum('quantity')).order_by('-quantity')[:10]
    return render(request, 'reports/profit_report.html', {
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'profit': total_revenue - total_expenses,
        'best_sellers': best_sellers,
    })


@login_required
def export_csv(request):
    report_type = request.GET.get('type', 'sales')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report.csv"'
    writer = csv.writer(response)

    if report_type == 'sales':
        writer.writerow(['Sale Number', 'Date', 'Customer', 'Total Amount'])
        for sale in Sale.objects.select_related('customer').all():
            writer.writerow([sale.sale_number, sale.created_at.date(), sale.customer.name if sale.customer else 'Walk-in', sale.total_amount])
    elif report_type == 'expenses':
        writer.writerow(['Category', 'Vendor', 'Date', 'Amount'])
        for expense in Expense.objects.all():
            writer.writerow([expense.category, expense.vendor, expense.expense_date, expense.amount])
    else:
        writer.writerow(['Product', 'Quantity', 'Selling Price'])
        for product in Product.objects.all():
            writer.writerow([product.name, product.quantity, product.selling_price])
    return response
