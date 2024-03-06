from . import utils, models, forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q, Count
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def get_side_menu(ctx):
    result = []
    header = ctx.get('header', None)
    result.append({'description': _("All articles"), 'link': reverse(main_view), 'active': True if header == _("All articles") else False})
    menu_items = models.ArticleMenu.objects.filter(hide=False).all()
    for obj in menu_items:
        result.append({'description': obj.description, 'link': reverse('main_filtered', kwargs={'menu':obj.id}), 'active': True if header == obj.description else False})
    return result


def main_view(request):
    return main_filtered_view(request, None)


def main_filtered_view(request, menu):
    # Articles
    article_list = models.Article.objects.filter(published=True)
    header = _("All articles")
    if menu is not None:
        article_menu = get_object_or_404(models.ArticleMenu, pk=menu)
        article_list = article_list.filter(menu=article_menu)
        header = article_menu.description

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

    # News
    news_list = models.News.objects.filter(published=True)

    # Top 5 Articles
    top_articles = models.ArticleLog.objects.filter(article__published=True).values('article_id').annotate(total=Count('*')).order_by('-total')[:getattr(settings, 'SVJIS_TOP_ARTICLES_LIST_SIZE', 10)]
    for ta in top_articles:
        ta['article'] = get_object_or_404(models.Article, pk=ta['article_id'])

    ctx = {
        'aside_menu_name': _("Articles"),
    }
    ctx['is_paginated'] = is_paginated
    ctx['page_obj'] = page_obj
    ctx['page_parameter'] = page_parameter
    ctx['search_endpoint'] = reverse(main_view)
    ctx['search'] = search
    ctx['header'] = header
    ctx['article_list'] = article_list
    ctx['news_list'] = news_list
    ctx['top_articles'] = top_articles
    ctx['aside_menu_items'] = get_side_menu(ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu('articles', request.user)
    return render(request, "main.html", ctx)


def article_view(request, pk):
    article = get_object_or_404(models.Article, pk=pk)
    user = request.user
    if user.is_anonymous:
        user = None
    models.ArticleLog.objects.create(article=article, user=user)
    ctx = {
        'aside_menu_name': _("Articles"),
    }
    ctx['search'] = request.GET.get('search', '')
    ctx['header'] = article.menu.description
    ctx['obj'] = article
    ctx['aside_menu_items'] = get_side_menu(ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu('articles', request.user)
    return render(request, "article.html", ctx)

@permission_required("articles.svjis_add_article_comment")
def article_comment_save_view(request):
    article_pk = int(request.POST.get('article_pk'))
    if request.method == "POST":
        body = request.POST.get('body', '')
        if body != '':
            article = get_object_or_404(models.Article, pk=article_pk)
            models.ArticleComment.objects.create(body=body, article=article, author=request.user)
    return redirect(article_view, pk=article_pk)


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
