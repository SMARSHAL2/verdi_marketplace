from django.db import models
from django.conf import settings
from produtos.models import Produto

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('concluido', 'Concluído'),
    ]

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    finalizado = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    criado_em = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.produto.preco * item.quantidade for item in self.itens.all())

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.email} - {self.status}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def total_item(self):
        return self.produto.preco * self.quantidade

    def __str__(self):
        return f"{self.produto.nome} x {self.quantidade}"
