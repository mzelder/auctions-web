from django import forms
from .models import CATEGORY_CHOICES

class ListingForm(forms.Form): 
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description")
    starting_bid = forms.DecimalField(label="Starting Bid")
    image = forms.ImageField(label="Image", required=False)
    category = forms.ChoiceField(label="Category", choices=CATEGORY_CHOICES)