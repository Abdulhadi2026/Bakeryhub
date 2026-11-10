from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeForm
from .models import Employee


@login_required
def employee_list(request):
    query = request.GET.get('q', '').strip()
    employees = Employee.objects.order_by('name')
    if query:
        employees = employees.filter(Q(name__icontains=query) | Q(role__icontains=query) | Q(phone__icontains=query))
    return render(request, 'employees/employee_list.html', {'employees': employees, 'query': query})


@login_required
def employee_form(request, pk=None):
    employee = get_object_or_404(Employee, pk=pk) if pk else None
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            saved_employee = form.save()
            messages.success(request, f"Employee '{saved_employee.name}' saved successfully.")
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'employee': employee})


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    messages.success(request, 'Employee deleted successfully.')
    return redirect('employee_list')
