from . import utils, forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from django.urls import reverse


def get_side_menu(active_item):
    result = []
    result.append({'description': _("Users"), 'link': reverse(admin_user_view), 'active': True if active_item == 'users' else False})
    result.append({'description': _("Groups"), 'link': reverse(admin_group_view), 'active': True if active_item == 'groups' else False})
    return result


# Administration - User
def admin_user_view(request):
    if not request.user.is_superuser:
        raise Http404

    user_list = User.objects.all()
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
        i = get_object_or_404(User, pk=pk)
        form = forms.UserEditForm(instance=i)
    else:
        i = User
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
            instance = get_object_or_404(User, pk=pk)
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


# Administration - Group
def admin_group_view(request):
    if not request.user.is_superuser:
        raise Http404

    group_list = Group.objects.all()
    ctx = {
        'aside_menu_name': _("Administration"),
    }
    ctx['aside_menu_items'] = get_side_menu('groups')
    ctx['tray_menu_items'] = utils.get_tray_menu('admin', request.user)
    ctx['object_list'] = group_list
    return render(request, "admin_group.html", ctx)


def admin_group_edit_view(request, pk):
    if not request.user.is_superuser:
        raise Http404

    if pk != 0:
        i = get_object_or_404(Group, pk=pk)
        form = forms.GroupEditForm(instance=i)
    else:
        i = Group
        form = forms.GroupEditForm

    ctx = {
        'aside_menu_name': _("Administration"),
    }
    ctx['form'] = form
    ctx['instance'] = i
    ctx['pk'] = pk
    ctx['aside_menu_items'] = get_side_menu('groups')
    ctx['tray_menu_items'] = utils.get_tray_menu('admin', request.user)
    return render(request, "admin_group_edit.html", ctx)


def admin_group_save_view(request):
    if not request.user.is_superuser:
        raise Http404

    if request.method == "POST":
        pk = int(request.POST['pk'])
        if pk == 0:
            form = forms.GroupEditForm(request.POST)
        else:
            instance = get_object_or_404(Group, pk=pk)
            form = forms.GroupEditForm(request.POST, instance=instance)
        if form.is_valid:
            form.save()
        else:
            messages.error(request, _("Invalid form input"))
    return redirect(admin_group_view)


def admin_group_delete_view(request, pk):
    if not request.user.is_staff:
        raise Http404

    obj = get_object_or_404(Group, pk=pk)
    obj.delete()
    return redirect(admin_group_view)
