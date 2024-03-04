from . import utils, models, forms, views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Redaction - Article Menu
def redaction_menu_view(request):
    if not request.user.is_staff:
        return redirect(views.main_view)

    ctx = {
        'aside_menu_name': _("Redaction"),
    }
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_menu_view, ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_menu_view, request.user)
    ctx['object_list'] = models.ArticleMenu.objects.all()
    return render(request, "redaction_menu.html", ctx)


def redaction_menu_edit_view(request, pk):
    if not request.user.is_staff:
        return redirect(views.main_view)

    if pk != 0:
        am = get_object_or_404(models.ArticleMenu, pk=pk)
        form = forms.ArticleMenuForm(instance=am)
    else:
        form = forms.ArticleMenuForm

    ctx = {
        'aside_menu_name': _("Redaction"),
    }
    ctx['form'] = form
    ctx['pk'] = pk
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_menu_view, ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_menu_view, request.user)
    return render(request, "redaction_menu_edit.html", ctx)


def redaction_menu_save_view(request):
    if not request.user.is_staff:
        return redirect(views.main_view)

    if request.method == "POST":
        pk = int(request.POST['pk'])
        if pk == 0:
            form = forms.ArticleMenuForm(request.POST)
        else:
            instance = get_object_or_404(models.ArticleMenu, pk=pk)
            form = forms.ArticleMenuForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
        else:
            messages.error(request, _("Invalid form input"))

    return redirect(redaction_menu_view)


def redaction_menu_delete_view(request, pk):
    if not request.user.is_staff:
        return redirect(views.main_view)

    obj = get_object_or_404(models.ArticleMenu, pk=pk)
    obj.delete()
    return redirect(redaction_menu_view)


# Redaction - Article
def redaction_article_view(request):
    if not request.user.is_staff:
        return redirect(views.main_view)

    article_list = models.Article.objects.all()

    # Search
    search = request.POST.get('search')
    if search is None:
        search = request.GET.get('search')
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
        header = _("Article")

    # Paginator
    is_paginated = len(article_list) > getattr(settings, 'SVJIS_ARTICLE_PAGE_SIZE', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(article_list, per_page=getattr(settings, 'SVJIS_ARTICLE_PAGE_SIZE', 10))
    page_obj = paginator.get_page(page)
    try:
        article_list = paginator.page(page)
    except InvalidPage:
        article_list = paginator.page(paginator.num_pages)
    page_parameter = '' if search == '' else f"search={search}"

    ctx = {
        'aside_menu_name': _("Redaction"),
    }
    ctx['is_paginated'] = is_paginated
    ctx['page_obj'] = page_obj
    ctx['page_parameter'] = page_parameter
    ctx['search_endpoint'] = reverse(redaction_article_view)
    ctx['search'] = search
    ctx['header'] = header
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_article_view, ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_article_view, request.user)
    ctx['object_list'] = article_list
    return render(request, "redaction_article.html", ctx)


def redaction_article_edit_view(request, pk):
    if not request.user.is_staff:
        return redirect(views.main_view)

    if pk != 0:
        a = get_object_or_404(models.Article, pk=pk)
        form = forms.ArticleForm(instance=a)
    else:
        form = forms.ArticleForm

    ctx = {
        'aside_menu_name': _("Redaction"),
    }
    ctx['form'] = form
    ctx['pk'] = pk
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_article_view, ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_article_view, request.user)
    return render(request, "redaction_article_edit.html", ctx)


def redaction_article_save_view(request):
    if not request.user.is_staff:
        return redirect(views.main_view)

    if request.method == "POST":
        pk = int(request.POST['pk'])
        if pk == 0:
            form = forms.ArticleForm(request.POST)
        else:
            instance = get_object_or_404(models.Article, pk=pk)
            form = forms.ArticleForm(request.POST, instance=instance)

        if form.is_valid():
            obj = form.save(commit=False)
            if pk == 0:
                obj.author = request.user
            obj.save()
        else:
            for error in form.errors:
                messages.error(request, error)

    return redirect(redaction_article_view)


def redaction_article_delete_view(request, pk):
    if not request.user.is_staff:
        return redirect(views.main_view)

    obj = get_object_or_404(models.Article, pk=pk)
    obj.delete()
    return redirect(redaction_article_view)


# Redaction - MiniNews
def redaction_news_view(request):
    if not request.user.is_staff:
        return redirect(views.main_view)

    news_list = models.News.objects.all()
    header = _("News")

    # Paginator
    is_paginated = len(news_list) > getattr(settings, 'SVJIS_NEWS_PAGE_SIZE', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(news_list, per_page=getattr(settings, 'SVJIS_NEWS_PAGE_SIZE', 10))
    page_obj = paginator.get_page(page)
    try:
        news_list = paginator.page(page)
    except InvalidPage:
        news_list = paginator.page(paginator.num_pages)

    ctx = {
        'aside_menu_name': _("Redaction"),
    }
    ctx['is_paginated'] = is_paginated
    ctx['page_obj'] = page_obj
    ctx['header'] = header
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_news_view, ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_news_view, request.user)
    ctx['object_list'] = news_list
    return render(request, "redaction_news.html", ctx)


def redaction_news_edit_view(request, pk):
    if not request.user.is_staff:
        return redirect(views.main_view)

    if pk != 0:
        a = get_object_or_404(models.News, pk=pk)
        form = forms.NewsForm(instance=a)
    else:
        form = forms.NewsForm

    ctx = {
        'aside_menu_name': _("Redaction"),
    }
    ctx['form'] = form
    ctx['pk'] = pk
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_news_view, ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_news_view, request.user)
    return render(request, "redaction_news_edit.html", ctx)


def redaction_news_save_view(request):
    if not request.user.is_staff:
        return redirect(views.main_view)

    if request.method == "POST":
        pk = int(request.POST['pk'])
        if pk == 0:
            form = forms.NewsForm(request.POST)
        else:
            instance = get_object_or_404(models.News, pk=pk)
            form = forms.NewsForm(request.POST, instance=instance)

        if form.is_valid():
            obj = form.save(commit=False)
            if pk == 0:
                obj.author = request.user
            obj.save()
        else:
            for error in form.errors:
                messages.error(request, error)

    return redirect(redaction_news_view)


def redaction_news_delete_view(request, pk):
    if not request.user.is_staff:
        return redirect(views.main_view)

    obj = get_object_or_404(models.News, pk=pk)
    obj.delete()
    return redirect(redaction_news_view)
