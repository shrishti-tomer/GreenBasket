from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import CartItem
from products.models import Product

from .forms import CheckoutForm
from .models import Order, OrderItem


def checkout(request):

    session_key = request.session.session_key

    if not session_key:
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')

    cart_items = CartItem.objects.filter(
        session_key=session_key
    ).select_related('product')

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')

    total_price = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    if request.method == 'POST':

        form = CheckoutForm(request.POST)

        if form.is_valid():

            try:
                with transaction.atomic():

                    order = form.save(commit=False)
                    order.total_amount = total_price
                    order.save()

                    for item in cart_items:

                        product = Product.objects.get(
                            id=item.product.id
                        )

                        if product.stock_quantity < item.quantity:
                            raise ValueError(
                                f"Not enough stock for {product.name}."
                            )

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item.quantity,
                            price=product.price
                        )

                        product.stock_quantity -= item.quantity
                        product.save()

                    cart_items.delete()

                request.session['last_order_id'] = order.id

                return redirect(
                    'order_success',
                    order_id=order.id
                )

            except ValueError as error:
                messages.error(request, str(error))
                return redirect('cart_detail')

    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(
        request,
        'orders/checkout.html',
        context
    )


def order_success(request, order_id):

    if request.session.get('last_order_id') != order_id:
        return redirect('store_home')

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        'orders/order_success.html',
        {'order': order}
    )
