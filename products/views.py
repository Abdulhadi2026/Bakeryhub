from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, ProductForm
from .models import Category, Product


def _product_image_url(product):
    if product.image and getattr(product.image, 'url', None):
        return product.image.url

    name = (product.name or '').lower().strip()
    category = (product.category.name if product.category else '').lower()
    text = f"{name} {category}"

    image_map = {
        'amala': 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80',
        'eba': 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80',
        'semo': 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80',
        'tuwo shinkafa': 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=900&q=80',
        'white rice': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=900&q=80',
        'fried rice': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=900&q=80',
        'jollof rice': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=900&q=80',
        'coconut rice': 'https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=900&q=80',
        'yam porridge': 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80',
        'fried yam': 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80',
        'boiled yam': 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80',
        'beans porridge': 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80',
        'vegetable soup': 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80',
        'egusi soup': 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80',
        'okra soup': 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80',
        'plantain': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80',
        'fish roll': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=80',
        'meat pie': 'https://images.unsplash.com/photo-1517433670267-08bbd4be890f?auto=format&fit=crop&w=900&q=80',
        'sausage roll': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=80',
        'buns': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=80',
        'chocolate cake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=900&q=80',
        'vanilla cake': 'https://images.unsplash.com/photo-1533134242443-d6dbc6d8a8c7?auto=format&fit=crop&w=900&q=80',
        'cupcake': 'https://images.unsplash.com/photo-1486427944299-d1955d23e34d?auto=format&fit=crop&w=900&q=80',
        'brownie': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=900&q=80',
        'croissant': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=80',
        'bread': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=900&q=80',
        'sourdough': 'https://images.unsplash.com/photo-1549931314-a545dcf3bc73?auto=format&fit=crop&w=900&q=80',
        'cinnamon roll': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=900&q=80',
        'donut': 'https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=900&q=80',
        'cookie': 'https://images.unsplash.com/photo-1499636136210-6d847e2b6d3c?auto=format&fit=crop&w=900&q=80',
        'cookies': 'https://images.unsplash.com/photo-1499636136210-6d847e2b6d3c?auto=format&fit=crop&w=900&q=80',
        'beef pie': 'https://images.unsplash.com/photo-1517433670267-08bbd4be890f?auto=format&fit=crop&w=900&q=80',
        'chicken pie': 'https://images.unsplash.com/photo-1517433670267-08bbd4be890f?auto=format&fit=crop&w=900&q=80',
        'fruit tart': 'https://images.unsplash.com/photo-1464306076886-da185f6a9d8d?auto=format&fit=crop&w=900&q=80',
        'cheesecake': 'https://images.unsplash.com/photo-1533134242443-d6dbc6d8a8c7?auto=format&fit=crop&w=900&q=80',
        'sandwich': 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=900&q=80',
        'burger': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=80',
        'pizza': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=900&q=80',
        'snack box': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80',
        'puff puff': 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=900&q=80',
        'plantain chips': 'https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=900&q=80',
        'spring roll': 'https://images.unsplash.com/photo-1529042410759-befb1204b468?auto=format&fit=crop&w=900&q=80',
        'pastry': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=80',
    }

    for key, image_url in image_map.items():
        if key in name or key in text:
            return image_url

    if any(keyword in text for keyword in ['cake', 'cupcake', 'dessert', 'sweet']):
        return 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=900&q=80'
    if any(keyword in text for keyword in ['bread', 'loaf', 'toast', 'bun']):
        return 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=900&q=80'
    if any(keyword in text for keyword in ['cookie', 'biscuit']):
        return 'https://images.unsplash.com/photo-1499636136210-6d847e2b6d3c?auto=format&fit=crop&w=900&q=80'
    if any(keyword in text for keyword in ['pie', 'tart', 'pastry', 'roll', 'croissant']):
        return 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=80'
    if any(keyword in text for keyword in ['snack', 'sandwich', 'savoury', 'burger', 'pizza', 'sausage']):
        return 'https://images.unsplash.com/photo-1529042410759-befb1204b468?auto=format&fit=crop&w=900&q=80'
    return 'https://images.unsplash.com/photo-1517433670267-08bbd4be890f?auto=format&fit=crop&w=900&q=80'


def product_list(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.select_related('category').order_by('-created_at')
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(sku__icontains=query)
            | Q(category__name__icontains=query)
        )

    for product in products:
        product.image_url = _product_image_url(product)

    featured_products = list(products[:3])
    return render(request, 'products/product_list.html', {
        'products': products,
        'featured_products': featured_products,
        'query': query,
    })


@login_required
def product_form(request, pk=None):
    product = get_object_or_404(Product, pk=pk) if pk else None
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            save_product = form.save()
            messages.success(request, f"Product '{save_product.name}' saved successfully.")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'product': product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('product_list')


@login_required
def category_list(request):
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'products/category_list.html', {'categories': categories})


@login_required
def category_form(request, pk=None):
    category = get_object_or_404(Category, pk=pk) if pk else None
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            save_category = form.save()
            messages.success(request, f"Category '{save_category.name}' saved successfully.")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/category_form.html', {'form': form, 'category': category})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully.')
    return redirect('category_list')
