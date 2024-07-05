from . import utils, models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q, Count
from django.conf import settings
from django.http import Http404
from django.urls import reverse
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_POST
from datetime import datetime, timedelta


def get_side_menu(ctx):
    result = []
    header = ctx.get('header', None)
    result.append(
        {
            'description': _("All articles"),
            'link': reverse(main_view),
            'active': True if header == _("All articles") else False,
        }
    )
    menu_items = models.ArticleMenu.objects.filter(hide=False).all()
    for obj in menu_items:
        if obj.parent is None:
            active = True if header == obj.description else False
            node = {
                'description': obj.description,
                'link': reverse('main_filtered', kwargs={'menu': obj.id}),
                'active': active,
            }
            submenu = get_side_submenu(obj, menu_items, header, active)
            if submenu is not None:
                node['active'] = True
                node['submenu'] = submenu
            result.append(node)
    return result


def get_side_submenu(parent, menu_items, active_header, active):
    result = []
    for obj in menu_items:
        if obj.parent == parent:
            node = {
                'description': obj.description,
                'link': reverse('main_filtered', kwargs={'menu': obj.id}),
                'active': False,
            }
            if active_header == obj.description:
                active = True
            result.append(node)
    return result if active else None


def get_article_filter(user):
    q1 = Q(published=True)
    q2 = Q(visible_for_all=True)
    groups = Group.objects.filter(user__id=user.id)
    q3 = Q(visible_for_group__in=groups)
    return Q(q1 & (q2 | q3)) if not user.is_anonymous else Q(q1 & q2)


@require_GET
def main_view(request):
    return main_filtered_view(request, None)


@require_GET
def main_filtered_view(request, menu):
    # Articles
    q = get_article_filter(request.user)
    article_list = models.Article.objects.filter(q).distinct()

    # Top 5 Articles
    top_history_from = make_aware(
        datetime.now() - timedelta(days=getattr(settings, 'SVJIS_TOP_ARTICLES_HISTORY_IN_DAYS', 365))
    )
    top = (
        models.ArticleLog.objects.filter(entry_time__gte=top_history_from)
        .filter(article__published=True)
        .values('article_id')
        .annotate(total=Count('*'))
        .order_by('-total')
    )
    users_articles = [a.id for a in article_list]
    top_articles = [a for a in top if a['article_id'] in users_articles][
        : getattr(settings, 'SVJIS_TOP_ARTICLES_LIST_SIZE', 10)
    ]
    for ta in top_articles:
        ta['article'] = get_object_or_404(models.Article, pk=ta['article_id'])

    # Menu
    header = _("All articles")
    if menu is not None:
        article_menu = get_object_or_404(models.ArticleMenu, pk=menu)
        article_list = article_list.filter(menu=article_menu)
        header = article_menu.description

    # Search
    search = request.GET.get('search')
    if search is not None and len(search) < 3:
        messages.error(request, _("Search: Keyword '{}' is too short. Type at least 3 characters.").format(search))
        search = None
    if search is not None and len(search) > 100:
        messages.error(request, _("Search: Keyword is too long. Type maximum of 100 characters."))
        search = None
    if search is not None:
        qs = Q(header__icontains=search) | Q(perex__icontains=search) | Q(body__icontains=search)
        article_list = article_list.filter(qs)
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

    # Survey
    survey_list = models.Survey.objects.filter(published=True)
    slist = []
    for s in survey_list:
        node = {}
        node['survey'] = s
        node['user_can_vote'] = s.is_user_open_for_voting(request.user) if not request.user.is_anonymous else False
        slist.append(node)

    # Useful Links
    useful_links_list = models.UsefulLink.objects.filter(published=True)

    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Articles")
    ctx['is_paginated'] = is_paginated
    ctx['page_obj'] = page_obj
    ctx['page_parameter'] = page_parameter
    ctx['search_endpoint'] = reverse(main_view)
    ctx['search'] = search
    ctx['header'] = header
    ctx['article_list'] = article_list
    ctx['news_list'] = news_list
    ctx['survey_list'] = slist
    ctx['useful_links_list'] = useful_links_list
    ctx['top_articles'] = top_articles
    ctx['aside_menu_items'] = get_side_menu(ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu('articles', request.user)
    return render(request, "main.html", ctx)


@permission_required("articles.svjis_answer_survey")
@require_POST
def article_survey_vote_view(request):
    pk = int(request.POST.get('pk'))
    o_pk = int(request.POST.get(f'i_{pk}'))
    option = get_object_or_404(models.SurveyOption, pk=o_pk)
    survey = option.survey

    # is voting open?
    if not survey.is_open_for_voting:
        raise Http404

    # already voted?
    if not survey.is_user_open_for_voting(request.user):
        raise Http404

    models.SurveyAnswerLog.objects.create(survey=survey, option=option, user=request.user)
    return redirect(main_view)


@require_GET
def article_view(request, slug):
    if request.user.has_perm("articles.svjis_edit_article"):
        article_qs = models.Article.objects.filter(slug=slug)
    else:
        q = get_article_filter(request.user)
        article_qs = models.Article.objects.filter(Q(slug=slug) & q).distinct()

    if len(article_qs) == 0:
        raise Http404
    else:
        article = article_qs[0]

    user = request.user
    if user.is_anonymous:
        user = None

    models.ArticleLog.objects.create(article=article, user=user)
    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Articles")
    ctx['search'] = request.GET.get('search', '')
    ctx['header'] = article.menu.description
    ctx['obj'] = article
    ctx['assets'] = utils.wrap_assets(article.assets)
    ctx['web_title'] = article.header
    ctx['aside_menu_items'] = get_side_menu(ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu('articles', request.user)
    return render(request, "article.html", ctx)


@permission_required("articles.svjis_add_article_comment")
@require_POST
def article_comment_save_view(request):
    article_pk = int(request.POST.get('article_pk'))
    body = request.POST.get('body', '')
    if body != '':
        article = get_object_or_404(models.Article, pk=article_pk)
        comment = models.ArticleComment.objects.create(body=body, article=article, author=request.user)

        recipients = [u for u in article.watching_users.all() if u != request.user]
        utils.send_article_comment_notification(
            recipients, f"{request.scheme}://{request.get_host()}", article, comment
        )

    return redirect(reverse(article_watch_view) + f"?id={article_pk}&watch=1")


@permission_required("articles.svjis_add_article_comment")
@require_GET
def article_watch_view(request):
    try:
        pk = int(request.GET.get('id'))
        watch = int(request.GET.get('watch'))
    except TypeError:
        raise Http404

    q = get_article_filter(request.user)
    article_qs = models.Article.objects.filter(Q(pk=pk) & q).distinct()
    if len(article_qs) == 0:
        raise Http404
    else:
        article = article_qs[0]

    if watch == 0:
        article.watching_users.remove(request.user)
    else:
        article.watching_users.add(request.user)

    return redirect(article_view, slug=article.slug)


# Login
@require_POST
def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        messages.error(request, _("Wrong username or password"))
        messages.info(request, _("In case password is expired use Lost Password link"))
    return redirect(main_view)


@require_POST
def user_logout(request):
    logout(request)
    return redirect(main_view)


# Error pages
def error_404_view(request, exception):
    ctx = utils.get_context()
    ctx['tray_menu_items'] = utils.get_tray_menu('_', request.user)
    return render(request, "error_404.html", ctx, status=404)
