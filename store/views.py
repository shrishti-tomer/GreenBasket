
from django.shortcuts import render
from products.models import Product, Category


def store_home(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    # Get search and category values from the customer
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')

    # Search products by name
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Filter products by category
    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }

    return render(request, 'store/store_home.html', context)
