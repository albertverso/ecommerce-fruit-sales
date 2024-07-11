from django import forms
from ecommerce.models import User, Fruit, Sale, SaleItem
from django.forms import inlineformset_factory

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name']  # Campos que deseja permitir a edição


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['last_name'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})


class FruitForm(forms.ModelForm):
    class Meta:
        model = Fruit
        fields = ['image', 'fruit_name', 'rating', 'quantity', 'itemssalevalue_sale', 'fresh']

    def __init__(self, *args, **kwargs):
        super(FruitForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['fruit_name'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['rating'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['itemssalevalue_sale'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['quantity'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['fresh'].widget.attrs.update({'class': 'p-10 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
       

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['date_time', 'total_value']

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['total_value'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['fruit', 'quantity', 'unitary_value', 'discount']

    def __init__(self, *args, **kwargs):
        super(SaleItemForm, self).__init__(*args, **kwargs)
        self.fields['fruit'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['quantity'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['unitary_value'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['discount'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
    


SaleItemFormSet = inlineformset_factory(Sale, SaleItem, form=SaleItemForm, extra=1, can_delete=True)


class FrutaFilterForm(forms.Form):
    nome = forms.CharField(required=False)
    classificacao = forms.CharField(required=False)
    fresca = forms.BooleanField(required=False)
    preco_min = forms.DecimalField(decimal_places=2, required=False)
    preco_max = forms.DecimalField(decimal_places=2, required=False)

    def __init__(self, *args, **kwargs):
        super(FrutaFilterForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'h-[38px] w-full border-transparent rounded-full bg-white focus:outline-none text-lg text-black absolute'})