from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SupplierForm
from .models import Supplier


@login_required
def supplier_list(request):
    query = request.GET.get('q', '').strip()
    suppliers = Supplier.objects.order_by('name')
    if query:
        suppliers = suppliers.filter(Q(name__icontains=query) | Q(contact_person__icontains=query) | Q(phone__icontains=query))
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers, 'query': query})


@login_required
def supplier_form(request, pk=None):
    supplier = get_object_or_404(Supplier, pk=pk) if pk else None
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            saved_supplier = form.save()
            messages.success(request, f"Supplier '{saved_supplier.name}' saved successfully.")
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/supplier_form.html', {'form': form, 'supplier': supplier})


@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    messages.success(request, 'Supplier deleted successfully.')
    return redirect('supplier_list')
