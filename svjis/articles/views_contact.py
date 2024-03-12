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


def get_side_menu(active_item, user):
    result = []
    result.append({'description': _("Contact"), 'link': reverse(contact_view), 'active': True if active_item == 'company' else False})
    if user.has_perm('articles.svjis_view_phonelist'):
        result.append({'description': _("Phonelist"), 'link': reverse(phonelist_view), 'active': True if active_item == 'phonelist' else False})
    return result


# Contact - company
@require_GET
def contact_view(request):
    instance, created = models.Company.objects.get_or_create(pk=1)
    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Contact")
    ctx['company'] = instance
    ctx['aside_menu_items'] = get_side_menu('company', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('contact', request.user)
    return render(request, "contact_company.html", ctx)


# Contact - phonelist
@permission_required("articles.svjis_view_phonelist")
@require_GET
def phonelist_view(request):
    phone_list = User.objects.filter(is_active=True, userprofile__show_in_phonelist=True).order_by('last_name')
    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Contact")
    ctx['object_list'] = phone_list
    ctx['aside_menu_items'] = get_side_menu('phonelist', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('contact', request.user)
    return render(request, "contact_phonelist.html", ctx)

