from django import forms

from gadgets.models import Gadget, Gift, Purchase


class GadgetForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    model = forms.CharField(max_length=255, required=False)
    brand = forms.CharField(max_length=255, required=False)
    free_form = forms.CharField(widget=forms.Textarea, required=False)
    acquisition_type = forms.ChoiceField(
        choices=Gadget.AcquisitionType.choices)

    class Meta:
        model = Gadget
        fields = ['name', 'model', 'brand', 'free_form', 'acquisition_type']


class PurchaseForm(forms.ModelForm):
    date = forms.DateField()
    price_ati = forms.NumberInput()
    shop = forms.CharField(required=False)

    class Meta:
        model = Purchase
        fields = ['date', 'price_ati', 'shop']


class GiftForm(forms.ModelForm):
    date = forms.DateField()

    class Meta:
        model = Gift
        fields = ['date']
