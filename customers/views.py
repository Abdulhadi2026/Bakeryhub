from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomerForm
from .models import Customer


@login_required
def customer_list(request):
    query = request.GET.get('q', '').strip()
    customers = Customer.objects.order_by('name')
    if query:
        customers = customers.filter(Q(name__icontains=query) | Q(phone__icontains=query) | Q(email__icontains=query))
    return render(request, 'customers/customer_list.html', {'customers': customers, 'query': query})


@login_required
def customer_form(request, pk=None):
    customer = get_object_or_404(Customer, pk=pk) if pk else None
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            saved_customer = form.save()
            messages.success(request, f"Customer '{saved_customer.name}' saved successfully.")
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'customer': customer})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    messages.success(request, 'Customer deleted successfully.')
    return redirect('customer_list')
