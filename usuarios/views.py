from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from usuarios import views as usuarios_views
from .forms import EnderecoForm, UsuarioPerfilForm, UsuarioCreationForm
from .models import Endereco
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/register.html', {'form': form})


def register_produtor_view(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_produtor = True
            user.save()
            return redirect('login')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/register_produtor.html', {'form': form})

@login_required
def selecionar_endereco(request):
    if request.method == 'POST':
        endereco_id = request.POST.get('endereco_id')
        request.session['endereco_selecionado'] = endereco_id
    return redirect('perfil')

@login_required
def perfil_view(request):
    endereco_form = EnderecoForm()
    perfil_form = UsuarioPerfilForm(instance=request.user)

    # Adiciona um form separado para cada endereço (para edição)
    enderecos = request.user.enderecos.all()
    for endereco in enderecos:
        endereco.form = EnderecoForm(instance=endereco)

    context = {
        'user': request.user,
        'endereco_form': endereco_form,
        'perfil_form': perfil_form,
        'enderecos': enderecos,
    }
    return render(request, 'perfil/perfil.html', context)

@login_required
def adicionar_endereco(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.usuario = request.user
            endereco.save()
            messages.success(request, "Endereço adicionado com sucesso!")
        else:
            messages.error(request, "Erro ao adicionar endereço. Verifique os dados.")
    return redirect('perfil')


@login_required
def tornar_endereco_principal(request, endereco_id):
    endereco = get_object_or_404(Endereco, id=endereco_id, usuario=request.user)

    # Remove status principal de todos os endereços do usuário
    Endereco.objects.filter(usuario=request.user).update(principal=False)

    # Define o novo principal
    endereco.principal = True
    endereco.save()

    return redirect('perfil')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UsuarioPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
        else:
            messages.error(request, "Erro ao atualizar perfil.")
    return redirect('perfil')

@login_required
def editar_endereco(request, endereco_id):
    endereco = get_object_or_404(Endereco, id=endereco_id, usuario=request.user)
    if request.method == 'POST':
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            messages.success(request, "Endereço atualizado com sucesso.")
        else:
            messages.error(request, "Erro ao atualizar endereço.")
    return redirect('perfil')
