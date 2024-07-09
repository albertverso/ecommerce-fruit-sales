from django import forms
from ecommerce.models import User, Fruit, Sale, SaleItem

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name']  # Campos que deseja permitir a edição


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})
        self.fields['last_name'].widget.attrs.update({'class': 'p-2 border  rounded-lg focus:outline-none focus-within:border-[#A7C957]'})