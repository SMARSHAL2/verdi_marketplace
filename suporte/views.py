from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from usuarios.models import Usuario 
from .models import PromocaoSistema
from .forms import PromocaoSistemaForm
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json


# ✅ Verifica se o usuário é suporte
def is_suporte(user):
    return user.is_authenticated and user.is_suporte

# ✅ Painel de suporte
@login_required
@user_passes_test(is_suporte)
def dashboard(request):
    total_usuarios = Usuario.objects.count()
    total_vendedores = Usuario.objects.filter(is_produtor=True).count()
    
    return render(request, 'suporte/dashboard.html', {
        'total_usuarios': total_usuarios,
        'total_vendedores': total_vendedores,
        'total_vendas': '-',  # Apenas um placeholder temporário
    })

# ✅ Exibe formulário
@login_required
@user_passes_test(is_suporte)
def cadastro_usuario_form(request):
    return render(request, 'suporte/cadastro_usuario.html')

@login_required
@user_passes_test(is_suporte)
def cadastrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        tipo = request.POST.get('tipo')
        senha = request.POST.get('senha')

        # Verifica se o email já existe
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Já existe um usuário com este e-mail.')
            return redirect('suporte_cadastro_usuario')

        # Cria o novo usuário com a senha fornecida
        usuario = Usuario.objects.create_user(
            email=email,
            password=senha,
            nome=nome
        )

        # Define se é agricultor/vendedor
        usuario.is_produtor = True if tipo == 'vendedor' else False
        usuario.save()

        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('painel_suporte')

    return redirect('painel_suporte')

@login_required
def desconto_sistema(request):
    if request.method == 'POST':
        form = PromocaoSistemaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('desconto_sistema')
    else:
        form = PromocaoSistemaForm()

    promocoes = PromocaoSistema.objects.order_by('-data_inicio')

    # Só considera como vigente se estiver ativa e dentro da data
    hoje = timezone.now().date()
    promocoes_vigentes = promocoes.filter(ativo=True, data_inicio__lte=hoje, data_fim__gte=hoje)


    return render(request, 'suporte/desconto_sistema.html', {
        'form': form,
        'promocoes_vigentes': promocoes_vigentes,
        'promocoes': promocoes,
    })


@login_required
def editar_promocao(request, promocao_id):
    promocao = get_object_or_404(PromocaoSistema, pk=promocao_id)
    if request.method == 'POST':
        form = PromocaoSistemaForm(request.POST, instance=promocao)
        if form.is_valid():
            form.save()
            return redirect('desconto_sistema')
    else:
        form = PromocaoSistemaForm(instance=promocao)

    return render(request, 'suporte/desconto_sistema_form.html', {
        'form': form,
        'promocao': promocao,
    })

@login_required
@csrf_exempt  # apenas se estiver usando JS puro sem Django Form
def desativar_promocao(request, promocao_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            ativo = data.get('ativo')

            if not isinstance(ativo, bool):
                return JsonResponse({'status': 'erro', 'mensagem': 'Valor inválido para "ativo"'}, status=400)

            promocao = get_object_or_404(PromocaoSistema, pk=promocao_id)
            promocao.ativo = ativo
            promocao.save()

            return JsonResponse({'status': 'ok', 'ativo': promocao.ativo})

        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=500)

    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)