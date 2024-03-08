from . import utils, forms, models
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST


def get_side_menu(active_item, user):
    result = []
    if user.has_perm('articles.svjis_view_personal_menu'):
        result.append({'description': _("Personal settings"), 'link': reverse(personal_settings_edit_view), 'active': True if active_item == 'settings' else False})
    if user.has_perm('articles.svjis_view_personal_menu'):
        result.append({'description': _("Password change"), 'link': reverse(personal_settings_password_view), 'active': True if active_item == 'password' else False})
    return result


# Personal settings - profile
@permission_required("articles.svjis_view_personal_menu")
@require_GET
def personal_settings_edit_view(request):
    ctx = {
        'aside_menu_name': _("Personal settings"),
    }
    ctx['aside_menu_items'] = get_side_menu('settings', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('personal_settings', request.user)
    return render(request, "personal_settings_edit.html", ctx)


@permission_required("articles.svjis_view_personal_menu")
@require_POST
def personal_settings_save_view(request):
    user_form = forms.PersonalUserForm(request.POST, instance=request.user)
    user_profile_form = forms.PersonalUserProfileForm(request.POST, instance=request.user.userprofile)

    if user_form.is_valid() and user_profile_form.is_valid():
        u = user_form.save()
        u.userprofile.save()
    else:
        for error in user_form.errors:
            messages.error(request, f"{_('Form validation error')}: {error}")
        for error in user_profile_form.errors:
            messages.error(request, f"{_('Form validation error')}: {error}")

    return redirect(personal_settings_edit_view)


# Personal settings - password
@permission_required("articles.svjis_view_personal_menu")
@require_GET
def personal_settings_password_view(request):
    ctx = {
        'aside_menu_name': _("Personal settings"),
    }
    ctx['aside_menu_items'] = get_side_menu('password', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('personal_settings', request.user)
    return render(request, "personal_settings_password.html", ctx)


@permission_required("articles.svjis_view_personal_menu")
@require_POST
def personal_settings_password_save_view(request):
    username = request.user.username
    pwd = request.POST.get("old_password")
    npwd1 = request.POST.get("new_password_1")
    npwd2 = request.POST.get("new_password_2")

    user = authenticate(username=username, password=pwd)
    if user is None:
        messages.error(request, _("Wrong password"))
        return redirect(personal_settings_password_view)

    if npwd1 == '':
        messages.error(request, _("Password cannot be enpty"))
        return redirect(personal_settings_password_view)

    if npwd1 != npwd2:
        messages.error(request, _("New passwords don't match"))
        return redirect(personal_settings_password_view)

    user.password = make_password(npwd1)
    user.save()
    return redirect(personal_settings_password_view)
