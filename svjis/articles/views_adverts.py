from . import utils, forms, models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST


def get_side_menu(active_item, user):
    result = []
    types = models.AdvertType.objects.all()
    for t in types:
        result.append({
            'description': t.description + f' ({models.Advert.objects.filter(published=True, type=t).count()})',
            'link': reverse(adverts_list_view),
            'active': True if active_item == t.pk else False})
    return result


# Faults - Fault report
@permission_required("articles.svjis_view_adverts_menu")
@require_GET
def adverts_list_view(request):
    advert_list = models.Advert.objects.all()

    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Adverts")
    ctx['aside_menu_items'] = get_side_menu(None, request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('adverts', request.user)
    ctx['object_list'] = advert_list
    return render(request, "adverts_list.html", ctx)
