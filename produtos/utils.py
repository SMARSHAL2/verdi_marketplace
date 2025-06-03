from suporte.models import PromocaoSistema
from django.utils import timezone

def calcular_desconto_aplicavel(desconto_produtor, desconto_sistema):
    """
    Retorna o desconto a ser aplicado:
    - Usa desconto_produtor se for maior que desconto_sistema.
    - Caso contrário, usa desconto_sistema.
    """
    if desconto_produtor >= desconto_sistema:
        return desconto_produtor
    return desconto_sistema


def get_desconto_sistema(categoria=None):
    hoje = timezone.now().date()
    promocoes = PromocaoSistema.objects.filter(
        ativo=True,
        data_inicio__lte=hoje,
        data_fim__gte=hoje
    )

    if categoria:
        promocoes = promocoes.filter(categorias=categoria)

    return promocoes.order_by('-data_inicio').first()
