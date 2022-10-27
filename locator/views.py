import os
from django.db.models import Q
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404

from locator.models import Post
from utils.pagination import makePagination

from locator.forms.login import LoginForm
from locator.forms.register import RegisterForm


QTY_PER_PAGE = int(os.environ.get('QTY_PER_PAGE', 4))


def home(request):
    posts = Post.objects.filter(published=True).order_by('-id')
    page, paginationInfo = makePagination(request, posts, QTY_PER_PAGE)
    return render(request, 'locator/pages/home.html', context={
        'page': page,
        'tinyRange': paginationInfo.get('tinyRange'),
        'paginationInfo': paginationInfo
    })


def post(request, id):
    post = get_object_or_404(Post, pk=id, published=True)
    return render(request, 'locator/pages/post.html', context={'post': post})


def search(request):
    searchTerm = request.GET.get('q', '').strip()

    if not searchTerm:
        raise Http404()

    posts = Post.objects.filter(Q(Q(title__icontains=searchTerm) | Q(description__icontains=searchTerm)), published=True)
    posts = posts.order_by('-id')
    page, paginationInfo = makePagination(request, posts, QTY_PER_PAGE)

    return render(request, 'locator/pages/home.html', context={
        'searchTerm': searchTerm,
        'page': page,
        'tinyRange': paginationInfo.get('tinyRange'),
        'paginationInfo': paginationInfo,
        'additionalParam': f"&q={searchTerm}"
    })


def registerForm(request):
    form_data = request.session.get('form_data')
    form = RegisterForm(form_data)
    return render(request, 'locator/pages/register.html', context={'form': form})


def registerAction(request):
    if not request.POST:
        raise Http404()

    form_data = request.POST
    request.session['form_data'] = form_data
    form = RegisterForm(form_data)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Seu usuário foi criado com sucesso, faça o login')
        del (request.session['form_data'])
        return redirect(reverse('loginForm'))

    return redirect('registerForm')


def loginForm(request):
    form = LoginForm()
    return render(request, 'locator/pages/login.html', context={'form': form})


def loginAction(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    if form.is_valid():
        authenticatedUser = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if authenticatedUser:
            login(request, authenticatedUser)
            messages.success(request, 'Usuário logado com sucesso')
        else:
            messages.error(request, 'Usuário inválido')

    else:
        messages.error(request, 'Erro na validação')

    return redirect(reverse('loginForm'))


@login_required(login_url='loginForm')
def logoutAction(request):
    if not request.POST:
        return redirect('loginForm')

    if request.POST.get('username') != request.user.username:
        return redirect('loginForm')

    logout(request)
    return redirect('loginForm')
