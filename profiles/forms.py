from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'phone': 'Phone Number',
            'address_line1': 'Address Line 1',
            'address_line2': 'Address Line 2',
            'city': 'City',
            'state': 'State / Province',
            'postal_code': 'Postal Code',
            'country': 'Country',
        }

        # Add autofocus to the first field (phone)
        self.fields['phone'].widget.attrs['autofocus'] = True

        # Loop through fields to add placeholders and classes
        for field_name, field in self.fields.items():
            placeholder = placeholders.get(field_name, '')
            if field.required:
                placeholder += ' *'
            field.widget.attrs['placeholder'] = placeholder
            field.widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            field.label = False
