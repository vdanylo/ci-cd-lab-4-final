from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('state', 'city', 'street', 'house', 'zip_code')
        widgets = {
            'house': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }
        labels = {
            'house': 'Будинок',
            'zip_code': 'Поштовий індекс',
            'state': 'Область',
            'city': 'Місто',
            'street': 'Вулиця',
        }
        help_texts = {
            'house': 'інформація про дім (номер поверху, під\'їзу)'
        }


class PaymentForm(forms.Form):

    card_number = forms.CharField(max_length=19,
                                  label='Номер картки',
                                  widget=forms.TextInput(
                                      attrs={'placeholder': 'XXXX-XXXX-XXXX-XXXX',
                                             'pattern': '[0-9]{4}-?[0-9]{4}-?[0-9]{4}-?[0-9]{4}',
                                             'class': 'form-control'}))
    expiry_date = forms.CharField(max_length=5,
                                  label='Дійсна до',
                                  widget=forms.TextInput(
                                   attrs={'placeholder': 'XX/XX',
                                          'pattern': '[0-9]{2}/[0-9]{2}',
                                          'class': 'form-control'}))
    cvv = forms.CharField(max_length=3,
                          label='CVV',
                          widget=forms.TextInput(attrs={'placeholder': 'XXX',
                                                        'pattern': '[0-9]{3}',
                                                        'class': 'form-control'}))
    error_messages = {
        'card_number': {
            'required': 'Це поле є обов\'язковим'
        },
        'expiry_date': {
            'required': 'Це поле є обов\'язковим'
        },
        'cvv': {
            'required': 'Це поле є обов\'язковим'
        }
    }
