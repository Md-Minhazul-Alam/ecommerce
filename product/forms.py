from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import Review, Product, Brand, Category, Tag
from .widgets import CustomClearableFileInput


# Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your experience with this product...',
                'required': True,
            }),
        }
        labels = {
            'rating': 'Your Rating',
            'comment': 'Your Review',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].required = True
        self.fields['comment'].required = True
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Field('rating'),
            Field('comment'),
        )


# Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'brand',
            'category',
            'tags',
            'price',
            'rating',
            'short_description',
            'description',
            'has_variation',
            'thumbnail',
            'image_url',
            'is_active',
            'is_featured',
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={
                'placeholder': 'Enter product name',
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01',
            }),
            'rating': forms.NumberInput(attrs={
                'placeholder': '0.00',
                'min': '0',
                'max': '5',
                'step': '0.01',
            }),
            'short_description': forms.TextInput(attrs={
                'placeholder': 'Short description (max 255 characters)',
            }),
            'image_url': forms.URLInput(attrs={
                'placeholder': (
                    'https://png.pngtree.com/png-vector/20190820/ourmid/'
                    'pngtree-no-image-vector-illustration-isolated-'
                    'png-image_1694547.jpg'
                ),
            }),
            'tags': forms.CheckboxSelectMultiple(),
            'has_variation': forms.Select(choices=[
                ('', 'Select'),
                ('True', 'Yes'),
                ('False', 'No'),
            ]),
            'thumbnail': CustomClearableFileInput(),
        }
        labels = {
            'product_name': 'Product Name',
            'brand': 'Brand',
            'category': 'Category',
            'tags': 'Tags',
            'price': 'Price',
            'rating': 'Rating',
            'short_description': 'Short Description',
            'description': 'Description',
            'has_variation': 'Has Variation',
            'thumbnail': 'Thumbnail Image',
            'image_url': 'Image URL (or provide thumbnail above)',
            'is_active': 'Active',
            'is_featured': 'Featured',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.filter(is_active=True)
        self.fields['category'].queryset = Category.objects.filter(
            is_active=True
        )
        self.fields['tags'].queryset = Tag.objects.filter(is_active=True)
        self.fields['brand'].empty_label = 'Select Brand'
        self.fields['category'].empty_label = 'Select Category'

        # Required fields
        self.fields['product_name'].required = True
        self.fields['brand'].required = True
        self.fields['category'].required = True
        self.fields['price'].required = True
        self.fields['short_description'].required = True
        self.fields['description'].required = True
        self.fields['has_variation'].required = True
        self.fields['tags'].required = True

        # Optional fields
        self.fields['rating'].required = False
        self.fields['is_active'].required = False
        self.fields['is_featured'].required = False

        # thumbnail and image_url individually optional
        # but at least one required — enforced in clean()
        self.fields['thumbnail'].required = False
        self.fields['image_url'].required = False

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Field('product_name'),
            Field('brand'),
            Field('category'),
            Field('tags'),
            Field('price'),
            Field('rating'),
            Field('short_description'),
            Field('description'),
            Field('thumbnail'),
            Field('image_url'),
            Field('has_variation'),
            Field('is_active'),
            Field('is_featured'),
        )

    def clean(self):
        cleaned_data = super().clean()
        thumbnail = cleaned_data.get('thumbnail')
        image_url = cleaned_data.get('image_url')
        rating = cleaned_data.get('rating')

        if not thumbnail and not image_url:
            raise forms.ValidationError(
                'Please provide either a Thumbnail image or an Image URL.'
            )

        if rating is not None and (rating < 0 or rating > 5):
            self.add_error('rating', 'Rating must be between 0 and 5.')

        return cleaned_data