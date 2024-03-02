from . import utils, models, forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def main_view(request):
    return main_filtered_view(request, None)


def main_filtered_view(request, menu):
    article_list = models.Article.objects.filter(published=True)
    header = _("All articles")
    if menu is not None:
        article_menu = get_object_or_404(models.ArticleMenu, pk=menu)
        article_list = article_list.filter(menu=article_menu)
        header = article_menu.description
    search = request.POST.get('search_field')
    if search is not None and len(search) < 3:
        messages.error(request, _("Search: Keyword '{}' is too short. Type at least 3 characters.").format(search))
        search = None
    if search is not None and len(search) > 100:
            messages.error(request, _("Search: Keyword is too long. Type maximum of 100 characters."))
            search = None
    if search is not None:
        article_list = article_list.filter(Q(header__icontains=search) | Q(perex__icontains=search) | Q(body__icontains=search))
        header = _("Search results") + f": {search}"
    else:
        search = ''
    ctx = {
        'aside_menu_name': _("Articles"),
    }
    ctx['search_endpoint'] = reverse(main_view)
    ctx['search'] = search
    ctx['header'] = header
    ctx['article_list'] = article_list
    ctx['aside_menu_items'] = utils.get_aside_menu(main_view, ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu(main_view, request.user)
    return render(request, "main.html", ctx)


def article_view(request, pk):
    article = get_object_or_404(models.Article, pk=pk)
    ctx = {
        'aside_menu_name': _("Articles"),
    }
    ctx['search'] = request.GET.get('search', '')
    ctx['header'] = article.menu.description
    ctx['obj'] = article
    ctx['aside_menu_items'] = utils.get_aside_menu(main_view, ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu(main_view, request.user)
    return render(request, "article.html", ctx)


# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
    return redirect(main_view)


def user_logout(request):
    logout(request)
    return redirect(main_view)
