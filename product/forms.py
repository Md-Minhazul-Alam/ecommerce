from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your experience with this product...'
            }),
        }
        labels = {
            'rating': 'Your Rating',
            'comment': 'Your Review',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('rating', css_class='d-flex gap-3'),
            Field('comment'),
            Submit('submit', 'Submit Review', css_class='btn btn-primary mt-2')
        )