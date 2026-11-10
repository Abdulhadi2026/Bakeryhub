from django.db import models
from django.utils import timezone


class Expense(models.Model):
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vendor = models.CharField(max_length=150, blank=True)
    expense_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-expense_date',)

    def __str__(self):
        return f"{self.category} - {self.amount}"
