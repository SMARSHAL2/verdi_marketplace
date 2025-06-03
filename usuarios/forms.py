from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Endereco

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'password1', 'password2')

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        exclude = ['usuario']

class UsuarioPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'cpf', 'telefone', 'nascimento']