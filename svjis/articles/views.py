from . import utils, models, forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout



def main_view(request):
    article_list = models.Article.objects.filter(published=True).all()
    ctx = {
        'aside_menu_name': 'Články',
    }
    ctx['aside_menu_items'] = utils.get_aside_menu(main_view)
    ctx['tray_menu_items'] = utils.get_tray_menu(main_view)
    ctx['article_list'] = article_list
    return render(request, "main.html", ctx)


def article_view(request, pk):
    article = get_object_or_404(models.Article, pk=pk)
    ctx = {
        'aside_menu_name': 'Články',
    }
    ctx['obj'] = article
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_article_view)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_article_view)
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


# Redaction - Article Menu
def redaction_menu_view(request):
    ctx = {
        'aside_menu_name': 'Redakce',
    }
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_menu_view)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_menu_view)
    ctx['object_list'] = models.ArticleMenu.objects.all()
    return render(request, "redaction_menu.html", ctx)


def redaction_menu_edit_view(request, pk):
    if pk != 0:
        am = get_object_or_404(models.ArticleMenu, pk=pk)
        form = forms.ArticleMenuForm(instance=am)
    else:
        form = forms.ArticleMenuForm

    ctx = {
        'aside_menu_name': 'Redakce',
    }
    ctx['form'] = form
    ctx['pk'] = pk
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_menu_view)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_menu_view)
    return render(request, "redaction_menu_edit.html", ctx)


def redaction_menu_save_view(request):
    if request.method == "POST":
        form = forms.ArticleMenuForm(request.POST)
        if form.is_valid():
            pk = int(request.POST['pk'])
            description = request.POST.get('description', '')
            hide = request.POST.get('hide', False) == 'on'
            parent = request.POST['parent']
            if parent == '':
                parent = None
            else:
                parent = get_object_or_404(models.ArticleMenu, pk=int(parent))
            if pk == 0:
                models.ArticleMenu.objects.create(description=description, hide=hide, parent=parent)
            else:
                models.ArticleMenu.objects.filter(id=pk).update(description=description, hide=hide, parent=parent)
    return redirect(redaction_menu_view)


def redaction_menu_delete_view(request, pk):
    obj = get_object_or_404(models.ArticleMenu, pk=pk)
    obj.delete()
    return redirect(redaction_menu_view)


# Redaction - Article
def redaction_article_view(request):
    ctx = {
        'aside_menu_name': 'Redakce',
    }
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_article_view)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_article_view)
    ctx['object_list'] = models.Article.objects.all()
    return render(request, "redaction_article.html", ctx)


def redaction_article_edit_view(request, pk):
    if pk != 0:
        a = get_object_or_404(models.Article, pk=pk)
        form = forms.ArticleForm(instance=a)
    else:
        form = forms.ArticleForm

    ctx = {
        'aside_menu_name': 'Redakce',
    }
    ctx['form'] = form
    ctx['pk'] = pk
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_article_view)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_article_view)
    return render(request, "redaction_article_edit.html", ctx)


def redaction_article_save_view(request):
    if request.method == "POST":
        form = forms.ArticleForm(request.POST)
        if form.is_valid():
            pk = int(request.POST['pk'])
            header = request.POST.get('header', '')
            perex = request.POST.get('perex', '')
            body = request.POST.get('body', '')
            published = request.POST.get('published', False) == 'on'
            author = request.user
            menu = get_object_or_404(models.ArticleMenu, pk=int(request.POST['menu']))
            if pk == 0:
                models.Article.objects.create(header=header, perex=perex, body=body, menu=menu, published=published, author=author)
            else:
                models.Article.objects.filter(id=pk).update(header=header, perex=perex, body=body, menu=menu, published=published, author=author)
    return redirect(redaction_article_view)


def redaction_article_delete_view(request, pk):
    obj = get_object_or_404(models.Article, pk=pk)
    obj.delete()
    return redirect(redaction_article_view)
