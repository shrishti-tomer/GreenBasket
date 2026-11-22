
from django.db.models import Sum
from django.shortcuts import render

from .models import Product


def dashboard(request):
    total_products = Product.objects.count()

    total_stock_units = Product.objects.aggregate(
        total=Sum('stock_quantity')
    )['total'] or 0

    low_stock_products = Product.objects.filter(
        stock_quantity__gt=0,
        stock_quantity__lte=10
    ).count()
    low_stock_items = Product.objects.filter(
        stock_quantity__gt=0,
        stock_quantity__lte=10
    ).order_by('stock_quantity')

    out_of_stock_products = Product.objects.filter(
        stock_quantity=0
    ).count()
    latest_products = Product.objects.select_related('category').order_by('-id')[:5]

    context = {
        'total_products': total_products,
        'total_stock_units': total_stock_units,
        'low_stock_products': low_stock_products,
        'low_stock_items': low_stock_items,
        'out_of_stock_products': out_of_stock_products,
        'latest_products': latest_products,
    }

    return render(request, 'products/dashboard.html', context)

def product_list(request):
    products = Product.objects.select_related('category').all()

    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')

    if search_query:
        products = products.filter(name__icontains=search_query)

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Product.objects.values(
        'category__id',
        'category__name'
    ).distinct()

    context = {
        'products': products,
        'search_query': search_query,
        'categories': categories,
        'selected_category': category_id,
    }

    return render(request, 'products/product_list.html', context)