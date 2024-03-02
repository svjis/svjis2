from . import utils, models, forms, views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Administration - User
def admin_user_view(request):
    if not request.user.is_superuser:
        return redirect(views.main_view)

    user_list = get_user_model().objects.all()
    ctx = {
        'aside_menu_name': _("Administration"),
    }
    ctx['aside_menu_items'] = utils.get_aside_menu(admin_user_view, ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu(admin_user_view, request.user)
    ctx['object_list'] = user_list
    return render(request, "admin_user.html", ctx)


def admin_user_edit_view(request, pk):
    if not request.user.is_superuser:
        return redirect(views.main_view)

    if pk != 0:
        i = get_object_or_404(get_user_model(), pk=pk)
        form = forms.UserEditForm(instance=i)
    else:
        i = get_user_model()
        form = forms.UserCreateForm

    ctx = {
        'aside_menu_name': _("Administration"),
    }
    ctx['form'] = form
    ctx['instance'] = i
    ctx['pk'] = pk
    ctx['aside_menu_items'] = utils.get_aside_menu(admin_user_view, ctx)
    ctx['tray_menu_items'] = utils.get_tray_menu(admin_user_view, request.user)
    return render(request, "admin_user_edit.html", ctx)


def admin_user_save_view(request):
    if not request.user.is_superuser:
        return redirect(views.main_view)

    if request.method == "POST":
        pk = int(request.POST['pk'])
        if pk == 0:
            form = forms.UserCreateForm(request.POST)
        else:
            instance = get_object_or_404(get_user_model(), pk=pk)
            form = forms.UserEditForm(request.POST, instance=instance)
        if form.is_valid:
            form.save()
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            active = request.POST.get('active', False) == 'on'
            staff = request.POST.get('staff', False) == 'on'
            superuser = request.POST.get('superuser', False) == 'on'

            if pk == 0:
                instance = get_object_or_404(get_user_model().objects.filter(username=username))
            else:
                instance = get_object_or_404(get_user_model(), pk=pk)

            if password != '':
                instance.set_password(password)

            instance.is_active = active
            instance.is_staff = staff
            instance.is_superuser = superuser
            instance.save()
        else:
            messages.error(request, _("Invalid form input"))
    return redirect(admin_user_view)
