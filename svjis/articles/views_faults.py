from . import utils, forms, models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST


def get_side_menu(active_item, user):
    result = []
    if user.has_perm('articles.svjis_view_fault_menu'):
        result.append({
            'description': _("Open") + f' ({models.FaultReport.objects.filter(closed=False).count()})',
            'link': reverse(faults_list_view) + '?scope=open',
            'active': True if active_item == 'open' else False})
        if user.has_perm('articles.svjis_fault_reporter'):
            result.append({
                'description': _("Mine") + f' ({models.FaultReport.objects.filter(closed=False, created_by_user=user).count()})',
                'link': reverse(faults_list_view) + '?scope=mine',
                'active': True if active_item == 'mine' else False})
        if user.has_perm('articles.svjis_fault_resolver'):
            result.append({
                'description': _("Assigned to me") + f' ({models.FaultReport.objects.filter(closed=False, assigned_to_user=user).count()})',
                'link': reverse(faults_list_view) + '?scope=assigned',
                'active': True if active_item == 'assigned' else False})
        result.append({
            'description': _("Closed") + f' ({models.FaultReport.objects.filter(closed=True).count()})',
            'link': reverse(faults_list_view) + '?scope=closed',
            'active': True if active_item == 'closed' else False})
    return result


# Faults - Fault report
@permission_required("articles.svjis_view_fault_menu")
@require_GET
def faults_list_view(request):
    fault_list = models.FaultReport.objects.all()
    scope = request.GET.get('scope', '')
    if scope == 'open':
        fault_list = fault_list.filter(closed=False)
    if scope == 'mine':
        fault_list = fault_list.filter(created_by_user=request.user)
    if scope == 'assigned':
        fault_list = fault_list.filter(assigned_to_user=request.user)
    if scope == 'closed':
        fault_list = fault_list.filter(closed=True)


    # Search
    search = request.GET.get('search')
    if search is not None and len(search) < 3:
        messages.error(request, _("Search: Keyword '{}' is too short. Type at least 3 characters.").format(search))
        search = None
    if search is not None and len(search) > 100:
            messages.error(request, _("Search: Keyword is too long. Type maximum of 100 characters."))
            search = None
    if search is not None:
        fault_list = fault_list.filter(Q(subject__icontains=search) | Q(description__icontains=search))
        header = _("Search results") + f": {search}"
    else:
        search = ''
        header = _("Fault reporting")

    # Paginator
    is_paginated = len(fault_list) > getattr(settings, 'SVJIS_FAULTS_PAGE_SIZE', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(fault_list, per_page=getattr(settings, 'SVJIS_FAULTS_PAGE_SIZE', 10))
    page_obj = paginator.get_page(page)
    try:
        fault_list = paginator.page(page)
    except InvalidPage:
        fault_list = paginator.page(paginator.num_pages)
    page_parameter = f'scope={scope}' if search == '' else f"search={search}"

    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Fault reporting")
    ctx['header'] = header
    ctx['is_paginated'] = is_paginated
    ctx['page_obj'] = page_obj
    ctx['page_parameter'] = page_parameter
    ctx['search_endpoint'] = reverse(faults_list_view)
    ctx['search'] = search
    ctx['aside_menu_items'] = get_side_menu(scope, request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('faults', request.user)
    ctx['object_list'] = fault_list
    return render(request, "faults_list.html", ctx)


@permission_required("articles.svjis_view_fault_menu")
@require_GET
def fault_view(request, slug):
    fault_qs = models.FaultReport.objects.filter(slug=slug)
    if len(fault_qs) == 0:
        raise Http404
    else:
        fault = fault_qs[0]

    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Fault reporting")
    ctx['aside_menu_items'] = get_side_menu('faults', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('faults', request.user)
    ctx['obj'] = fault
    ctx['search'] = request.GET.get('search', '')
    ctx['assets'] = utils.wrap_assets(fault.assets)
    ctx['asset_form'] = forms.FaultAssetForm
    return render(request, "fault.html", ctx)


@permission_required("articles.svjis_fault_resolver")
@require_GET
def faults_fault_edit_view(request, pk):
    if pk != 0:
        a = get_object_or_404(models.FaultReport, pk=pk)
        form = forms.FaultReportEditForm(instance=a)
    else:
        form = forms.FaultReportEditForm

    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Fault reporting")
    ctx['form'] = form
    ctx['pk'] = pk
    ctx['aside_menu_items'] = get_side_menu('faults', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('faults', request.user)
    return render(request, "faults_edit.html", ctx)


@permission_required("articles.svjis_fault_reporter")
@require_GET
def faults_fault_create_view(request):
    form = forms.FaultReportForm
    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Fault reporting")
    ctx['form'] = form
    ctx['pk'] = 0
    ctx['aside_menu_items'] = get_side_menu('faults', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('faults', request.user)
    return render(request, "faults_create.html", ctx)


@permission_required("articles.svjis_fault_reporter")
@require_POST
def faults_fault_save_view(request):
    pk = int(request.POST['pk'])
    if pk == 0:
        form = forms.FaultReportForm(request.POST)
    else:
        instance = get_object_or_404(models.FaultReport, pk=pk)
        form = forms.FaultReportForm(request.POST, instance=instance)

    if form.is_valid():
        obj = form.save(commit=False)
        if pk == 0:
            obj.created_by_user = request.user
        obj.save()
    else:
        for error in form.errors:
            messages.error(request, error)

    # Set watching users
    if pk == 0:
        obj.watching_users.add(request.user)
        resolvers = User.objects.filter(groups__permissions__codename='svjis_fault_resolver').exclude(is_active=False).distinct()
        for u in resolvers:
            obj.watching_users.add(u)

    # Send notifications
    recipients = []
    for u in obj.watching_users.all():
        if u.pk != request.user.pk:
            recipients.append(u)
    utils.send_new_fault_notification(recipients, f"{request.scheme}://{request.get_host()}", obj)

    return redirect(reverse(faults_list_view) + '?scope=open')


@permission_required("articles.svjis_fault_resolver")
@require_POST
def faults_fault_update_view(request):
    pk = int(request.POST['pk'])
    instance = get_object_or_404(models.FaultReport, pk=pk)
    form = forms.FaultReportEditForm(request.POST, instance=instance)

    if form.is_valid():
        form.save()
    else:
        for error in form.errors:
            messages.error(request, error)
    return redirect(reverse(faults_list_view) + '?scope=open')


# Faults - FaultAsset
@permission_required("articles.svjis_fault_reporter")
@require_POST
def faults_fault_asset_save_view(request):
    fault_pk = int(request.POST.get('fault_pk'))
    fault = get_object_or_404(models.FaultReport, pk=fault_pk)
    form = forms.FaultAssetForm(request.POST, request.FILES)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.fault_report = fault
        obj.created_by_user = request.user
        obj.save()
    else:
        for error in form.errors:
            messages.error(request, error)
    return redirect(fault_view, slug=fault.slug)


@permission_required("articles.svjis_fault_reporter")
@require_GET
def faults_fault_asset_delete_view(request, pk):
    obj = get_object_or_404(models.FaultAsset, pk=pk)
    fault_slug = obj.fault_report.slug
    if obj.created_by_user == request.user:
        obj.delete()
    return redirect(fault_view, slug=fault_slug)


# Faults - FaultComment
@permission_required("articles.svjis_add_fault_comment")
@require_POST
def fault_comment_save_view(request):
    fault_pk = int(request.POST.get('fault_pk'))
    body = request.POST.get('body', '')
    if body != '':
        fault = get_object_or_404(models.FaultReport, pk=fault_pk)
        comment = models.FaultComment.objects.create(body=body, fault_report=fault, author=request.user)

        recipients = []
        for u in fault.watching_users.all():
            if u.pk != request.user.pk:
                recipients.append(u)
        utils.send_fault_comment_notification(recipients, f"{request.scheme}://{request.get_host()}", fault, comment)

    return redirect(reverse(fault_watch_view) + f"?id={fault_pk}&watch=1")


# Faults - FaultWatching
@permission_required("articles.svjis_view_fault_menu")
@require_GET
def fault_watch_view(request):
    try:
        pk = int(request.GET.get('id'))
        watch = int(request.GET.get('watch'))
    except:
        raise Http404

    fault = get_object_or_404(models.FaultReport, pk=pk)

    if watch == 0:
        fault.watching_users.remove(request.user)
    else:
        fault.watching_users.add(request.user)

    return redirect(fault_view, slug=fault.slug)


# Faults - Take ticket
@permission_required("articles.svjis_fault_resolver")
@require_GET
def faults_fault_take_ticket_view(request, pk):
    fault = get_object_or_404(models.FaultReport, pk=pk)
    fault.assigned_to_user=request.user
    fault.save()
    return redirect(fault_view, slug=fault.slug)


# Faults - Close ticket
@permission_required("articles.svjis_fault_resolver")
@require_GET
def faults_fault_close_ticket_view(request, pk):
    fault = get_object_or_404(models.FaultReport, pk=pk)
    fault.closed=True
    fault.save()
    return redirect(fault_view, slug=fault.slug)
