from django import forms
from .models import Product

_base_input = "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-green-600"
_base_select = "w-full px-4 py-2 border border-gray-300 rounded-md bg-white focus:outline-none focus:border-green-600"
_base_checkbox = "w-5 h-5 text-green-600 rounded border-gray-300 focus:ring-0 cursor-pointer"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "thumbnail", "category",
                  "is_featured", "stock", "brand", "rating"]
        
        widgets = {
            "name": forms.TextInput(attrs={"class": _base_input, "placeholder": "Nama produk"}),
            "price": forms.NumberInput(attrs={"class": _base_input, "min": 0}),
            "description": forms.Textarea(attrs={"class": _base_input, "rows": 5, "placeholder": "Deskripsi..."}),
            "thumbnail": forms.URLInput(attrs={"class": _base_input, "placeholder": "https://..."}),
            "category": forms.TextInput(attrs={"class": _base_input, "placeholder": "Sepatu, Jersey, dll."}),
            "stock": forms.NumberInput(attrs={"class": _base_input, "min": 0}),
            "brand": forms.TextInput(attrs={"class": _base_input}),
            "rating": forms.NumberInput(attrs={"class": _base_input, "step": "0.1", "min": 0, "max": 5}),
            "is_featured": forms.CheckboxInput(attrs={"class": _base_checkbox}),
        }