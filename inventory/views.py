from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .forms import InventoryForm, StockMovementForm
from .models import Inventory, StockMovement


@login_required
def inventory_list(request):
    query = request.GET.get('q', '').strip()
    inventories = Inventory.objects.select_related('product').order_by('product__name')
    if query:
        inventories = inventories.filter(
            Q(product__name__icontains=query) | Q(product__sku__icontains=query)
        )
    low_stock = inventories.filter(quantity__lte=F('min_stock'))
    return render(request, 'inventory/inventory_list.html', {
        'inventories': inventories,
        'low_stock': low_stock,
        'query': query,
    })


@login_required
def stock_movement_form(request, pk=None):
    stock_movement = get_object_or_404(StockMovement, pk=pk) if pk else None
    if request.method == 'POST':
        form = StockMovementForm(request.POST, instance=stock_movement)
        if form.is_valid():
            movement = form.save()
            messages.success(request, f"Stock movement '{movement.product.name}' recorded.")
            return redirect('inventory_list')
    else:
        form = StockMovementForm(instance=stock_movement)
    return render(request, 'inventory/stock_movement_form.html', {'form': form, 'movement': stock_movement})


@login_required
def stock_movement_delete(request, pk):
    movement = get_object_or_404(StockMovement, pk=pk)
    movement.delete()
    messages.success(request, 'Stock movement deleted successfully.')
    return redirect('inventory_list')
