from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Order

        fields = [
            'customer_name',
            'email',
            'phone',
            'delivery_address',
        ]

        widgets = {
            'customer_name': forms.TextInput(attrs={
                'placeholder': 'Enter your full name'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address'
            }),

            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter your phone number'
            }),

            'delivery_address': forms.Textarea(attrs={
                'placeholder': 'Enter your complete delivery address',
                'rows': 4
            }),
        }