from django import forms
from .models import Restaurant, Item

class RestaurantSelectForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'name'
        ]

class ItemSelectForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name'
        ]