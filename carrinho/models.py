from django.db import models
from django.conf import settings
from produtos.models import Produto

class ItemCarrinho(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="itens_carrinho_usuario"
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="itens_carrinho_produto"
    )
    quantidade = models.PositiveIntegerField(default=1)

    @property
    def total_sem_desconto(self):
        return self.quantidade * self.produto.preco

    def total_com_desconto(self):
        desconto = self.produto.desconto_produtor or 0
        preco_com_desconto = self.produto.preco * (1 - desconto / 100)
        return self.quantidade * preco_com_desconto

    def __str__(self):
        return f"{self.produto.nome} x {self.quantidade}"
