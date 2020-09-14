from django import forms


class ItemForm(forms.Form):
    title = forms.CharField()
    price = forms.IntegerField()
    photo = forms.ImageField()
