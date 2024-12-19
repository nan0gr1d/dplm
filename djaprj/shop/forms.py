from django import forms

class ProductAdd(forms.Form):
    title = forms.CharField(max_length=30, label='Product title:')
    description = forms.CharField(label='Product description:')
    price = forms.IntegerField(label='Product price (in roubles):')

