
"""
URL configuration for GreenBasket.
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from products import views

urlpatterns = [
    # Homepage redirects to the dashboard
    path(
        '',
        RedirectView.as_view(url='/dashboard/', permanent=False),
        name='home',
    ),

    # Django administration
    path('admin/', admin.site.urls),

    # Product management
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),

    # Store functionality
    path('store/', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
]
