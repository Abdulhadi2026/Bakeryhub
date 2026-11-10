from django.db import models

from products.models import Product


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=10)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('product__name',)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} in stock"


class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjust', 'Adjustment'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES, default='in')
    quantity = models.PositiveIntegerField(default=0)
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.product.name} {self.movement_type} {self.quantity}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        inventory, _ = Inventory.objects.get_or_create(product=self.product)
        if self.movement_type == 'in':
            inventory.quantity += self.quantity
        elif self.movement_type == 'out':
            inventory.quantity = max(0, inventory.quantity - self.quantity)
        elif self.movement_type == 'adjust':
            inventory.quantity = self.quantity
        inventory.min_stock = self.product.min_stock
        inventory.save()
        self.product.quantity = inventory.quantity
        self.product.save()
