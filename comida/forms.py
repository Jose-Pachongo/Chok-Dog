from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import MensajeContacto

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        required=False, max_length=15, label="Número de Teléfono"
    )
    address = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": 2}), label="Dirección"
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'address', 'password1', 'password2']


class MensajeContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'correo', 'telefono', 'mensaje']
