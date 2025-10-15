from django.db import models
from usuarios.models import Usuario
from suporte.models import PromocaoSistema
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    desconto_produtor = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0,
        help_text='Desconto dado pelo produtor (%)'
    )
    estoque = models.PositiveIntegerField()
    imagem = models.ImageField(upload_to='produtos/')
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    def preco_com_desconto(self):
        hoje = timezone.now().date()
        promocao = (
            PromocaoSistema.objects.filter(
                ativo=True,
                data_inicio__lte=hoje,
                data_fim__gte=hoje,
                categorias=self.categoria
            )
            .order_by('-data_inicio')
            .first()
        )
        desconto_sistema = float(promocao.desconto) if promocao else 0.0
        desconto_aplicado = max(float(self.desconto_produtor), desconto_sistema)
        return float(self.preco) * (1 - desconto_aplicado / 100)

class ItemCarrinho(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def total_item(self, desconto_sistema=0.0):
        preco_unitario = self.produto.preco_com_desconto()  # usa o método do Produto sem parâmetros
        return preco_unitario * self.quantidade

class Avaliacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nota = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        null=True,
        blank=True 
    )
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nome} avaliou {self.produto.nome}"