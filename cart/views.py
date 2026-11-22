
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .models import CartItem


def add_to_cart(request, product_id):

    if request.method != 'POST':
        return redirect('store_home')

    product = get_object_or_404(Product, id=product_id)

    if product.stock_quantity < 1:
        messages.error(request, "This product is out of stock.")
        return redirect('store_home')

    if not request.session.session_key:
        request.session.create()

    cart_item, created = CartItem.objects.get_or_create(
        session_key=request.session.session_key,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        if cart_item.quantity < product.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.error(request, "Maximum available stock reached.")
            return redirect('store_home')

    messages.success(request, f"{product.name} added to your cart!")

    return redirect('store_home')


def cart_detail(request):

    session_key = request.session.session_key
    cart_items = []

    if session_key:
        cart_items = CartItem.objects.filter(
            session_key=session_key
        ).select_related('product')

    total_price = sum(
        item.subtotal() for item in cart_items
    )

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart/cart_detail.html', context)


def update_cart(request, item_id):

    if request.method != 'POST':
        return redirect('cart_detail')

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        session_key=request.session.session_key
    )

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        messages.error(request, "Please enter a valid quantity.")
        return redirect('cart_detail')

    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")

    elif quantity > cart_item.product.stock_quantity:
        messages.error(request, "Requested quantity exceeds available stock.")

    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart quantity updated successfully.")

    return redirect('cart_detail')


def remove_from_cart(request, item_id):

    if request.method != 'POST':
        return redirect('cart_detail')

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        session_key=request.session.session_key
    )

    cart_item.delete()

    messages.success(request, "Product removed from your cart.")

    return redirect('cart_detail')
