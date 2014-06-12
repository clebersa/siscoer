#coding:utf-8
from decimal import Decimal
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import timezone
from usuario.models import Usuario
from models import Localizacao, Categoria, Produto, Entrada, Baixa


@login_required
def start(request):
    username = request.user
    try:
        Usuario.objects.get(user__username=request.user)
        link = '/estoque/home/' + str(username)
        return redirect(link)
    except:
        link = '/login/'
        return redirect(link)


@login_required
def home(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    qtd_estoque = 0
    qtd_categorias = 0
    qtd_produtos = 0
    qtd_produtos_estoque = 0

    return render_to_response('index.html', locals(), context_instance=RequestContext(request),)


@login_required
def perfil(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    from forms import PerfilForm
    form = PerfilForm(instance=usuario)
    display = 'none;'
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.clean_imagem()
            afiliado = form.save()
            if afiliado:
                css = 'alert-success'
                display = 'block;'
                mostrar = 'Perfil atualizado com SUCESSO!'
                return render_to_response('perfil.html', locals(), context_instance=RequestContext(request),)
        else:
            css = 'alert-danger'
            display = 'block;'
            mostrar = 'Há campos obrigatórios não preenchidos, verifique abaixo.'
            return render_to_response('perfil.html', locals(), context_instance=RequestContext(request),)

    else:
        form = PerfilForm(instance=usuario)

    return render_to_response('perfil.html', locals(), context_instance=RequestContext(request),)


def cadastro(request):
    from forms import CadastroExternoForm
    form = CadastroExternoForm()
    display = 'none;'
    if request.method == 'POST':
        form = CadastroExternoForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            email = form.clean_mail()
            cad = Usuario(
                login = dados['login'],
                senha = dados['senha'],
                mail = dados['mail'],
                pergunta = dados['pergunta'],
                resposta = dados['resposta'],
            )
            cad.save()
            display = 'block;'
            mostrar = 'Obrigado! Cadastro efetuado com SUCESSO!'
            return render_to_response('cadastro_externo.html', locals(), context_instance=RequestContext(request))
    else:
        form = CadastroExternoForm()

    return render_to_response('cadastro_externo.html', locals(), context_instance=RequestContext(request),)


@login_required
def estoque(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    estoque = Localizacao.objects.all().exclude(ativo=False)

    return render_to_response('estoque.html', locals(), context_instance=RequestContext(request),)


@login_required
def cadastrar_estoque(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    from forms import CadastroEstoqueForm
    form = CadastroEstoqueForm()
    display = 'none;'
    if request.method == 'POST':
        form = CadastroEstoqueForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            cad = Localizacao(
                descricao = dados['descricao'],
            )
            cad.save()
            display = 'block;'
            mostrar = 'Obrigado! Cadastro efetuado com SUCESSO!'
            return render_to_response('cadastrar_estoque.html', locals(), context_instance=RequestContext(request))
    else:
        form = CadastroEstoqueForm()

    return render_to_response('cadastrar_estoque.html', locals(), context_instance=RequestContext(request),)


@login_required
def categoria(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    categoria = Categoria.objects.all().exclude(ativo=False)

    return render_to_response('categoria.html', locals(), context_instance=RequestContext(request),)


@login_required
def cadastrar_categoria(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    from forms import CadastroCategoriaForm
    form = CadastroCategoriaForm()
    display = 'none;'
    if request.method == 'POST':
        form = CadastroCategoriaForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            cad = Categoria(
                descricao = dados['descricao'],
            )
            cad.save()
            display = 'block;'
            mostrar = 'Obrigado! Cadastro efetuado com SUCESSO!'
            return render_to_response('cadastrar_categoria.html', locals(), context_instance=RequestContext(request))
    else:
        form = CadastroCategoriaForm()

    return render_to_response('cadastrar_categoria.html', locals(), context_instance=RequestContext(request),)


@login_required
def produto(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    produto = Produto.objects.all()

    return render_to_response('produto.html', locals(), context_instance=RequestContext(request),)


@login_required
def cadastrar_produto(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    from forms import CadastroProdutoForm
    form = CadastroProdutoForm()
    display = 'none;'
    if request.method == 'POST':
        form = CadastroProdutoForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            cad = Produto(
                categoria = dados['categoria'],
                descricao = dados['descricao'],
                unidade = dados['unidade'],
            )
            cad.save()
            display = 'block;'
            mostrar = 'Obrigado! Cadastro efetuado com SUCESSO!'
            return render_to_response('cadastrar_produto.html', locals(), context_instance=RequestContext(request))
    else:
        form = CadastroProdutoForm()

    return render_to_response('cadastrar_produto.html', locals(), context_instance=RequestContext(request),)


@login_required
def entrada(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    entrada = Entrada.objects.all().exclude(quantidade=0)

    return render_to_response('entrada.html', locals(), context_instance=RequestContext(request),)


@login_required
def cadastrar_entrada(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    from forms import CadastroEntradaForm
    form = CadastroEntradaForm()
    display = 'none;'
    if request.method == 'POST':
        form = CadastroEntradaForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            cad = Entrada(
                localizacao = dados['localizacao'],
                produto = dados['produto'],
                quantidade = dados['quantidade'],
                validade = dados['validade'],
                valor = dados['valor'],
                local_compra = dados['local_compra'],
                data_compra = dados['data_compra'],
            )
            cad.save()
            display = 'block;'
            mostrar = 'Obrigado! Cadastro efetuado com SUCESSO!'
            return render_to_response('cadastrar_entrada.html', locals(), context_instance=RequestContext(request))
    else:
        form = CadastroEntradaForm()

    return render_to_response('cadastrar_entrada.html', locals(), context_instance=RequestContext(request),)


@login_required
def baixa(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    baixa = Baixa.objects.all()

    return render_to_response('baixa.html', locals(), context_instance=RequestContext(request),)


@login_required
def cadastrar_baixa(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    from forms import CadastroBaixaForm
    form = CadastroBaixaForm()
    display = 'none;'
    if request.method == 'POST':
        form = CadastroBaixaForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            cad = Baixa(
                entrada = dados['entrada'],
                quantidade = dados['quantidade'],
                motivo = dados['motivo'],
            )
            cad.save()
            display = 'block;'
            mostrar = 'Obrigado! Cadastro efetuado com SUCESSO!'
            return render_to_response('cadastrar_baixa.html', locals(), context_instance=RequestContext(request))
    else:
        form = CadastroBaixaForm()

    return render_to_response('cadastrar_baixa.html', locals(), context_instance=RequestContext(request),)


@login_required
def ordem_alfabetica(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    produto = Entrada.objects.all().exclude(quantidade=0).order_by('produto__descricao')

    return render_to_response('ordem_alfabetica.html', locals(), context_instance=RequestContext(request),)


@login_required
def maior_qtd(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    produto = Entrada.objects.all().exclude(quantidade=0).order_by('-quantidade')

    return render_to_response('maior_qtd.html', locals(), context_instance=RequestContext(request),)


@login_required
def menor_qtd(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    produto = Entrada.objects.all().exclude(quantidade=0).order_by('quantidade')

    return render_to_response('menor_qtd.html', locals(), context_instance=RequestContext(request),)


@login_required
def proximo_vencer(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    produto = Entrada.objects.all().exclude(quantidade=0).order_by('validade')

    return render_to_response('proximo_vencer.html', locals(), context_instance=RequestContext(request),)


@login_required
def longe_vencer(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    produto = Entrada.objects.all().exclude(quantidade=0).order_by('-validade')

    return render_to_response('longe_vencer.html', locals(), context_instance=RequestContext(request),)


@login_required
def falta_alfabetica(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    produto = Produto.objects.all().filter(quantidade=0).order_by('descricao')

    return render_to_response('falta_alfabetica.html', locals(), context_instance=RequestContext(request),)


@login_required
def data_acabou(request, username):
    usuario = get_object_or_404(Usuario, user=request.user, user__username=username)

    produto = Produto.objects.all().filter(quantidade=0).order_by('alteracao')

    return render_to_response('data_acabou.html', locals(), context_instance=RequestContext(request),)






