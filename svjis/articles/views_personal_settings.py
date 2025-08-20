from . import utils, forms, models
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST


PERSONAL_SETTINGS_TEXT = "Personal settings"


def get_side_menu(active_item, user):
    result = []
    if user.has_perm('articles.svjis_view_personal_menu'):
        result.append(
            {
                'description': _(PERSONAL_SETTINGS_TEXT),
                'link': reverse(personal_settings_edit_view),
                'active': True if active_item == 'settings' else False,
            }
        )
        result.append(
            {
                'description': _("Language settings"),
                'link': reverse(personal_settings_lang_view),
                'active': True if active_item == 'lang' else False,
            }
        )
        result.append(
            {
                'description': _("My units"),
                'link': reverse(personal_my_units_view),
                'active': True if active_item == 'units' else False,
            }
        )
        result.append(
            {
                'description': _("Password change"),
                'link': reverse(personal_settings_password_view),
                'active': True if active_item == 'password' else False,
            }
        )
    return result


# Personal settings - profile
@permission_required("articles.svjis_view_personal_menu")
@require_GET
def personal_settings_edit_view(request):
    uform = forms.PersonalUserForm(instance=request.user)
    pinstance, _created = models.UserProfile.objects.get_or_create(user=request.user)
    pform = forms.PersonalUserProfileForm(instance=pinstance)
    ctx = utils.get_context()
    ctx['aside_menu_name'] = _(PERSONAL_SETTINGS_TEXT)
    ctx['uform'] = uform
    ctx['pform'] = pform
    ctx['aside_menu_items'] = get_side_menu('settings', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('personal_settings', request.user)
    return render(request, "personal_settings_edit.html", ctx)


@permission_required("articles.svjis_view_personal_menu")
@require_POST
def personal_settings_save_view(request):
    uform = forms.PersonalUserForm(request.POST, instance=request.user)
    pform = forms.PersonalUserProfileForm(request.POST, instance=request.user.userprofile)

    if uform.is_valid() and pform.is_valid():
        u = uform.save()
        u.userprofile.save()
        messages.info(request, _('Saved'))
    else:
        for error in uform.errors:
            messages.error(request, f"{_('Form validation error')}: {error}")
        for error in pform.errors:
            messages.error(request, f"{_('Form validation error')}: {error}")

    return redirect(personal_settings_edit_view)


# Personal settings - preferred language
@permission_required("articles.svjis_view_personal_menu")
@require_GET
def personal_settings_lang_view(request):
    ctx = utils.get_context()
    ctx['aside_menu_name'] = _(PERSONAL_SETTINGS_TEXT)
    ctx['aside_menu_items'] = get_side_menu('lang', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('personal_settings', request.user)
    return render(request, "personal_settings_language.html", ctx)


# Personal settings - my building units
@permission_required("articles.svjis_view_personal_menu")
@require_GET
def personal_my_units_view(request):
    ctx = utils.get_context()
    ctx['aside_menu_name'] = _(PERSONAL_SETTINGS_TEXT)
    ctx['aside_menu_items'] = get_side_menu('units', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('personal_settings', request.user)
    return render(request, "personal_my_units.html", ctx)


# Personal settings - password
@permission_required("articles.svjis_view_personal_menu")
@require_GET
def personal_settings_password_view(request):
    ctx = utils.get_context()
    ctx['aside_menu_name'] = _(PERSONAL_SETTINGS_TEXT)
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
    messages.info(request, _('Password has been changed'))
    return redirect(personal_settings_password_view)


@require_GET
def lost_password_view(request):
    ctx = utils.get_context()
    ctx['tray_menu_items'] = utils.get_tray_menu('_', request.user)
    return render(request, "send_lost_password.html", ctx)


@require_POST
def lost_password_send_view(request):
    email = request.POST.get("email")
    if not utils.validate_email_address(email):
        lmsg = _("E-Mail is not valid")
        messages.error(request, f"{lmsg}  {email}")
        return redirect(lost_password_view)
    u = User.objects.filter(email__iexact=email).exclude(is_active=False)
    if u is not None:
        for user in u:
            utils.send_new_password(user)
    messages.info(request, _("Credentials have been sent to your e-mail"))
    return redirect('/')
