from django import forms
from .models import Order
from .models import OrderLineItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'phone_number',
            'country',
            'postcode',
            'town_or_city',
            'street_address1',
            'street_address2',
            'county',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County / State / Region',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder': placeholders[field],
                'class': 'stripe-style-input',
            })
            self.fields[field].label = False


class OrderLineItemForm(forms.ModelForm):
    class Meta:
        model = OrderLineItem
        fields = ('product', 'product_variation', 'quantity')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'stripe-style-input'})
        self.fields['product_variation'].widget.attrs.update({'class': 'stripe-style-input'})
        self.fields['quantity'].widget.attrs.update({'class': 'stripe-style-input', 'min': 1})
