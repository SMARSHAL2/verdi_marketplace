from django import forms
from .models import PromocaoSistema

class PromocaoSistemaForm(forms.ModelForm):
    class Meta:
        model = PromocaoSistema
        fields = ['nome', 'desconto', 'data_inicio', 'data_fim', 'retroativa', 'ativo', 'categorias']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }
