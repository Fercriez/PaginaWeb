from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md', 'rows': 3
            }),
            'price': forms.NumberInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }