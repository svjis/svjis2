from . import utils, models, forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout



def main_view(request):
    ctx = {
        'aside_menu_name': 'Články',
    }
    ctx['aside_menu_items'] = utils.get_aside_menu(main_view)
    ctx['tray_menu_items'] = utils.get_tray_menu(main_view)
    return render(request, "main.html", ctx)


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


def redaction_view(request):
    ctx = {
        'aside_menu_name': 'Redakce',
    }
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_view)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_view)
    return render(request, "redaction.html", ctx)


def redaction_menu_view(request):
    ctx = {
        'aside_menu_name': 'Redakce',
    }
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_menu_view)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_menu_view)
    ctx['object_list'] = models.ArticleMenu.objects.all()
    return render(request, "redaction_menu.html", ctx)


def redaction_menu_edit_view(request, pk):
    ctx = {
        'aside_menu_name': 'Redakce',
    }
    ctx['form'] = forms.ArticleMenu
    ctx['pk'] = pk
    ctx['aside_menu_items'] = utils.get_aside_menu(redaction_menu_view)
    ctx['tray_menu_items'] = utils.get_tray_menu(redaction_menu_view)
    ctx['object_list'] = models.ArticleMenu.objects.all()
    return render(request, "redaction_menu_edit.html", ctx)


def redaction_menu_save_view(request):
    if request.method == "POST":
        form = forms.ArticleMenu(request.POST)
        if form.is_valid():
            pk = int(request.POST['pk'])
            description = request.POST.get('description', '')
            hide = request.POST.get('hide', False) == 'on'
            if pk == 0:
                 print("Creating")
                 models.ArticleMenu.objects.create(description=description, hide=hide)
    return redirect(redaction_menu_view)
