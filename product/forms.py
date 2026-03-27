from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import Review


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