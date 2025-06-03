from django.db import models
from django.utils import timezone
from django.apps import apps


class PromocaoSistema(models.Model):
    nome = models.CharField(max_length=255)
    desconto = models.DecimalField(max_digits=5, decimal_places=2)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    retroativa = models.BooleanField(default=False)
    ativo = models.BooleanField(default=False)
    categorias = models.ManyToManyField(
        'produtos.Categoria',
        blank=True,
        help_text="Deixe vazio para aplicar a todos os produtos"
    )

    def __str__(self):
        return f"{self.nome} ({self.desconto}%)"

    def esta_em_vigor(self):
        hoje = timezone.now().date()
        return self.ativo and self.data_inicio <= hoje <= self.data_fim

    def save(self, *args, **kwargs):
        if self.ativo:
            PromocaoSistema.objects.exclude(pk=self.pk).update(ativo=False)
        super().save(*args, **kwargs)

    def desativar(self):
        self.ativo = False
        self.save()