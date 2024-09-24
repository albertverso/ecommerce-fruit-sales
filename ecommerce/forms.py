from django import forms
from ecommerce.models import User, Fruit, Sale, SaleItem
from django.forms import inlineformset_factory

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'password', 'role']  # Campos que deseja permitir a edição
        widgets = {
            'password': forms.TextInput(attrs={'type': 'text',}),
            'email': forms.EmailInput(attrs={'type': 'email', 'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['last_name'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['email'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['password'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['role'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})

        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['role'].required = True

class FruitForm(forms.ModelForm):
    class Meta:
        model = Fruit
        fields = ['fruit_name', 'rating', 'quantity', 'itemssalevalue_sale', 'fresh', 'image']

    def __init__(self, *args, **kwargs):
        super(FruitForm, self).__init__(*args, **kwargs)
        self.fields['fruit_name'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['rating'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['itemssalevalue_sale'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['quantity'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['fresh'].widget.attrs.update({'class': 'p-10 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        
        self.fields['fruit_name'].required = True
        self.fields['rating'].required = True
        self.fields['itemssalevalue_sale'].required = True
        self.fields['fresh'].required = False
        self.fields['quantity'].required = True
        self.fields['image'].required = False
       

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['date_time', 'total_value']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'quantity': forms.NumberInput(attrs={
                'inputmode': 'numeric', 
                'min': '1', 
                'step': '1',
                'pattern': '[0-9]*'
            }),
            'total_value': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        self.fields['date_time'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['total_value'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]', 'type': 'datetime-local',})
        
        self.fields['date_time'].required = True
        self.fields['total_value'].required = True

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

        self.fields['fruit'].required = True
        self.fields['quantity'].required = True
        self.fields['unitary_value'].required = True
        self.fields['discount'].required = True
    

SaleItemFormSet = inlineformset_factory(Sale, SaleItem, form=SaleItemForm, extra=1, can_delete=True)
