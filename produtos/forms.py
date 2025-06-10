from django import forms
from .models import Produto
from .models import Avaliacao

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'imagem', 'categoria']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
        widgets = {
            'nota': forms.RadioSelect(choices=[(i, '⭐' * i) for i in range(1, 6)]),
            'comentario': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Deixe um comentário (opcional)',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comentario'].required = False

    def clean(self):
        cleaned_data = super().clean()
        nota = cleaned_data.get("nota")
        comentario = cleaned_data.get("comentario")

        if not nota and not comentario:
            raise forms.ValidationError("Você deve fornecer ao menos uma nota ou um comentário.")
