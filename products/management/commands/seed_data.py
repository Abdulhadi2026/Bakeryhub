from decimal import Decimal

from django.core.management.base import BaseCommand

from products.models import Category, Product


class Command(BaseCommand):
    help = 'Seed the bakery with sample categories and products.'

    def handle(self, *args, **options):
        categories = [
            ('Swallows', 'Traditional Nigerian swallow meals'),
            ('Rice Dishes', 'Cooked rice and rice combos'),
            ('Yam Dishes', 'Roasted, boiled and fried yam dishes'),
            ('Soups & Stews', 'Soup accompaniments for rice and swallow'),
            ('Snacks & Sides', 'Small bites and side orders'),
        ]

        created_categories = {}
        for name, description in categories:
            category, _ = Category.objects.get_or_create(name=name, defaults={'description': description})
            created_categories[name] = category

        products = [
            ('Amala', 'Swallows', 'AMA-001', Decimal('600'), Decimal('1400'), 35, 10),
            ('Eba', 'Swallows', 'EBA-001', Decimal('600'), Decimal('1400'), 30, 10),
            ('Semo', 'Swallows', 'SEM-001', Decimal('650'), Decimal('1600'), 25, 10),
            ('Tuwo Shinkafa', 'Swallows', 'TUW-001', Decimal('700'), Decimal('1700'), 24, 10),
            ('White Rice', 'Rice Dishes', 'RICE-001', Decimal('500'), Decimal('1200'), 40, 12),
            ('Fried Rice', 'Rice Dishes', 'FRI-001', Decimal('800'), Decimal('2000'), 28, 10),
            ('Jollof Rice', 'Rice Dishes', 'JOL-001', Decimal('750'), Decimal('1800'), 30, 12),
            ('Coconut Rice', 'Rice Dishes', 'COC-001', Decimal('850'), Decimal('2100'), 20, 8),
            ('Yam Porridge', 'Yam Dishes', 'YAM-001', Decimal('720'), Decimal('1800'), 22, 8),
            ('Fried Yam', 'Yam Dishes', 'FRY-001', Decimal('700'), Decimal('1700'), 26, 10),
            ('Boiled Yam', 'Yam Dishes', 'BOY-001', Decimal('680'), Decimal('1600'), 24, 10),
            ('Beans Porridge', 'Soups & Stews', 'BEA-001', Decimal('600'), Decimal('1500'), 25, 8),
            ('Vegetable Soup', 'Soups & Stews', 'VEG-001', Decimal('650'), Decimal('1600'), 18, 8),
            ('Egusi Soup', 'Soups & Stews', 'EGU-001', Decimal('900'), Decimal('2200'), 16, 8),
            ('Okra Soup', 'Soups & Stews', 'OKR-001', Decimal('750'), Decimal('1900'), 18, 8),
            ('Plantain', 'Snacks & Sides', 'PLA-001', Decimal('500'), Decimal('1100'), 32, 10),
            ('Fish Roll', 'Snacks & Sides', 'FIS-001', Decimal('350'), Decimal('800'), 28, 10),
            ('Meat Pie', 'Snacks & Sides', 'MEP-001', Decimal('450'), Decimal('1000'), 30, 10),
            ('Sausage Roll', 'Snacks & Sides', 'SAS-001', Decimal('380'), Decimal('900'), 26, 10),
            ('Buns', 'Snacks & Sides', 'BUN-001', Decimal('250'), Decimal('650'), 40, 12),
        ]

        for name, category_name, sku, cost, price, quantity, min_stock in products:
            Product.objects.update_or_create(
                sku=sku,
                defaults={
                    'name': name,
                    'category': created_categories[category_name],
                    'description': f'{name} is a popular meal served in the restaurant.',
                    'purchase_price': cost,
                    'selling_price': price,
                    'quantity': quantity,
                    'min_stock': min_stock,
                    'is_active': True,
                },
            )

        self.stdout.write(self.style.SUCCESS('Nigerian food sample data loaded successfully.'))
