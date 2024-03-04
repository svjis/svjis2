from . import utils, forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from django.urls import reverse


def get_side_menu(active_item):
    result = []
    result.append({'description': _("Users"), 'link': reverse(admin_user_view), 'active': True if active_item == 'users' else False})
    return result


# Administration - User
def admin_user_view(request):
    if not request.user.is_superuser:
        raise Http404

    user_list = get_user_model().objects.all()
    ctx = {
        'aside_menu_name': _("Administration"),
    }
    ctx['aside_menu_items'] = get_side_menu('users')
    ctx['tray_menu_items'] = utils.get_tray_menu('admin', request.user)
    ctx['object_list'] = user_list
    return render(request, "admin_user.html", ctx)


def admin_user_edit_view(request, pk):
    if not request.user.is_superuser:
        raise Http404

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
    ctx['aside_menu_items'] = get_side_menu('users')
    ctx['tray_menu_items'] = utils.get_tray_menu('admin', request.user)
    return render(request, "admin_user_edit.html", ctx)


def admin_user_save_view(request):
    if not request.user.is_superuser:
        raise Http404

    if request.method == "POST":
        pk = int(request.POST['pk'])
        if pk == 0:
            form = forms.UserCreateForm(request.POST)
        else:
            instance = get_object_or_404(get_user_model(), pk=pk)
            form = forms.UserEditForm(request.POST, instance=instance)
        if form.is_valid:
            instance = form.save()

            password = request.POST.get('password', '')
            active = request.POST.get('active', False) == 'on'
            staff = request.POST.get('staff', False) == 'on'
            superuser = request.POST.get('superuser', False) == 'on'

            if password != '':
                instance.set_password(password)

            instance.is_active = active
            instance.is_staff = staff
            instance.is_superuser = superuser
            instance.save()
        else:
            messages.error(request, _("Invalid form input"))
    return redirect(admin_user_view)
