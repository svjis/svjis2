from . import utils, forms, models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST


def get_side_menu(active_item, user):
    result = []
    result.append({
        'description': _("All") + f' ({models.Advert.objects.count()})',
        'link': reverse(adverts_list_view) + '?scope=all',
        'active': True if active_item == 'all' else False})

    types = models.AdvertType.objects.all()
    for t in types:
        result.append({
            'description': t.description + f' ({models.Advert.objects.filter(published=True, type=t).count()})',
            'link': reverse(adverts_list_view) + f'?scope={t.description}',
            'active': True if active_item == t.description else False})

    if user.has_perm('articles.svjis_add_advert'):
        result.append({
            'description': _("Mine") + f' ({models.Advert.objects.filter(published=True, created_by_user=user).count()})',
            'link': reverse(adverts_list_view)  + '?scope=mine',
            'active': True if active_item == 'mine' else False})

    return result


# Adverts
@permission_required("articles.svjis_view_adverts_menu")
@require_GET
def adverts_list_view(request):
    advert_list = models.Advert.objects.filter(published=True)
    scope = request.GET.get('scope', 'all')
    scope_description = _('All')

    if scope == 'mine':
        advert_list = models.Advert.objects.filter(created_by_user=request.user)
        scope_description = _('Mine')
    elif models.AdvertType.objects.filter(description=scope).count() > 0:
        advert_list = advert_list.filter(type__description=scope)
        scope_description = scope

    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Adverts")
    ctx['aside_menu_items'] = get_side_menu(scope, request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('adverts', request.user)
    ctx['object_list'] = advert_list
    ctx['scope_description'] = scope_description
    return render(request, "adverts_list.html", ctx)


@permission_required("articles.svjis_add_advert")
@require_GET
def adverts_edit_view(request, pk):
    if pk != 0:
        i = get_object_or_404(models.Advert, pk=pk)
        if i.created_by_user != request.user:
            raise Http404
        form = forms.AdvertForm(instance=i)
    else:
        form = forms.AdvertForm({'phone':request.user.userprofile.phone, 'email': request.user.email})

    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Adverts")
    ctx['form'] = form
    ctx['pk'] = pk
    ctx['aside_menu_items'] = get_side_menu(None, request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('adverts', request.user)
    return render(request, "advert_edit.html", ctx)


@permission_required("articles.svjis_add_advert")
@require_POST
def adverts_save_view(request):
    pk = int(request.POST['pk'])
    if pk == 0:
        form = forms.AdvertForm(request.POST)
    else:
        instance = get_object_or_404(models.Advert, pk=pk)
        if instance.created_by_user != request.user:
            raise Http404
        form = forms.AdvertForm(request.POST, instance=instance)

    if form.is_valid():
        obj = form.save(commit=False)
        if pk == 0:
            obj.created_by_user = request.user
        obj.save()
    else:
        for error in form.errors:
            messages.error(request, error)

    return redirect(reverse(adverts_list_view))
