from django import forms
from .models import Fruit


class FruitData(forms.ModelForm):
    class Meta:
        model = Fruit
        fields = ['name', 'origin', 'img']