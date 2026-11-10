from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExpenseForm
from .models import Expense


@login_required
def expense_list(request):
    query = request.GET.get('q', '').strip()
    expenses = Expense.objects.order_by('-expense_date')
    if query:
        expenses = expenses.filter(Q(category__icontains=query) | Q(vendor__icontains=query) | Q(description__icontains=query))
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'expenses/expense_list.html', {'expenses': expenses, 'query': query, 'total_expenses': total_expenses})


@login_required
def expense_form(request, pk=None):
    expense = get_object_or_404(Expense, pk=pk) if pk else None
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            saved_expense = form.save()
            messages.success(request, f"Expense '{saved_expense.category}' saved successfully.")
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form, 'expense': expense})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    messages.success(request, 'Expense deleted successfully.')
    return redirect('expense_list')
