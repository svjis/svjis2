from . import utils, forms, models
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from .permissions import svjis_view_adverts_menu, svjis_add_advert


def get_side_menu(active_item, user):
    description_template = '{} ({})'
    result = []
    result.append(
        {
            'description': description_template.format(
                _("All"), models.Advert.objects.filter(published=True, created_by_user__is_active=True).count()
            ),
            'link': reverse(adverts_list_view) + '?scope=all',
            'active': True if active_item == 'all' else False,
        }
    )

    types = models.AdvertType.objects.all()
    for t in types:
        result.append(
            {
                'description': description_template.format(
                    t.description,
                    models.Advert.objects.filter(published=True, created_by_user__is_active=True, type=t).count(),
                ),
                'link': reverse(adverts_list_view) + f'?scope={t.description}',
                'active': True if active_item == t.description else False,
            }
        )

    if user.has_perm(svjis_add_advert):
        result.append(
            {
                'description': description_template.format(
                    _("Mine"), models.Advert.objects.filter(created_by_user=user).count()
                ),
                'link': reverse(adverts_list_view) + '?scope=mine',
                'active': True if active_item == 'mine' else False,
            }
        )

    return result


# Adverts
@permission_required(svjis_view_adverts_menu)
@require_GET
def adverts_list_view(request):
    advert_list = models.Advert.objects.select_related('type', 'created_by_user').filter(
        published=True, created_by_user__is_active=True
    )
    scope = request.GET.get('scope', 'all')
    scope_description = _('All')

    if scope == 'mine':
        advert_list = models.Advert.objects.filter(created_by_user=request.user)
        scope_description = _('Mine')
    elif models.AdvertType.objects.filter(description=scope).count() > 0:
        advert_list = advert_list.filter(type__description=scope)
        scope_description = scope

    # Paginator
    is_paginated = len(advert_list) > getattr(settings, 'SVJIS_ADVERTS_PAGE_SIZE', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(advert_list, per_page=getattr(settings, 'SVJIS_ADVERTS_PAGE_SIZE', 10))
    page_obj = paginator.get_page(page)
    try:
        advert_list = paginator.page(page)
    except InvalidPage:
        advert_list = paginator.page(paginator.num_pages)
    page_parameter = f'scope={scope}'

    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Adverts")
    ctx['aside_menu_items'] = get_side_menu(scope, request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('adverts', request.user)
    ctx['is_paginated'] = is_paginated
    ctx['page_obj'] = page_obj
    ctx['page_parameter'] = page_parameter
    ctx['object_list'] = advert_list
    ctx['scope_description'] = scope_description
    return render(request, "adverts_list.html", ctx)


@permission_required(svjis_add_advert)
@require_GET
def adverts_edit_view(request, pk):
    if pk != 0:
        i = get_object_or_404(models.Advert, pk=pk)
        if i.created_by_user != request.user:
            raise Http404
        form = forms.AdvertForm(instance=i)
    else:
        form = forms.AdvertForm({'phone': request.user.userprofile.phone, 'email': request.user.email})

    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Adverts")
    ctx['form'] = form
    ctx['pk'] = pk
    ctx['asset_form'] = forms.AdvertAssetForm
    ctx['aside_menu_items'] = get_side_menu(None, request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('adverts', request.user)
    return render(request, "advert_edit.html", ctx)


@permission_required(svjis_add_advert)
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
        messages.info(request, _('Saved'))
    else:
        for error in form.errors:
            messages.error(request, error)

    return redirect(adverts_edit_view, pk=obj.pk)


# Adverts - AdvertAsset
@permission_required(svjis_add_advert)
@require_POST
def adverts_asset_save_view(request):
    advert_pk = int(request.POST.get('advert_pk'))
    advert = get_object_or_404(models.Advert, pk=advert_pk)
    if advert.created_by_user != request.user:
        raise Http404
    form = forms.AdvertAssetForm(request.POST, request.FILES)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.advert = advert
        obj.created_by_user = request.user
        obj.save()
        messages.info(request, _('Saved'))
    else:
        for error in form.errors:
            messages.error(request, error)
    return redirect(reverse('adverts_edit', kwargs={'pk': advert.pk}) + '#assets')


@permission_required(svjis_add_advert)
@require_GET
def adverts_asset_delete_view(request, pk):
    obj = get_object_or_404(models.AdvertAsset, pk=pk)
    advert = obj.advert
    if advert.created_by_user != request.user:
        raise Http404
    obj.delete()
    return redirect(reverse('adverts_edit', kwargs={'pk': advert.pk}) + '#assets')
