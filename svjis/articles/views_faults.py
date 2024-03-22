from . import utils, forms, models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST


def get_side_menu(active_item, user):
    result = []
    if user.has_perm('articles.svjis_view_fault_menu'):
        result.append({
            'description': _("Faults"),
            'link': reverse(faults_all_view),
            'active': True if active_item == 'faults' else False})
    return result


# Faults - Fault report
@permission_required("articles.svjis_view_fault_menu")
@require_GET
def faults_all_view(request):
    fault_list = models.FaultReport.objects.all()
    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Fault reporting")
    ctx['aside_menu_items'] = get_side_menu('faults', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('faults', request.user)
    ctx['object_list'] = fault_list
    return render(request, "faults_all.html", ctx)


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
    ctx['assets'] = utils.wrap_assets(fault.assets)
    ctx['asset_form'] = forms.FaultAssetForm
    return render(request, "fault.html", ctx)


@permission_required("articles.svjis_fault_reporter")
@require_GET
def faults_fault_edit_view(request, pk):
    if pk != 0:
        fr = get_object_or_404(models.FaultReport, pk=pk)
        form = forms.FaultReportForm(instance=fr)
    else:
        form = forms.FaultReportForm

    ctx = utils.get_context()
    ctx['aside_menu_name'] = _("Fault reporting")
    ctx['form'] = form
    ctx['pk'] = pk
    ctx['aside_menu_items'] = get_side_menu('faults', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('faults', request.user)
    return render(request, "faults_edit.html", ctx)


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
    return redirect(faults_all_view)


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

        for u in fault.watching_users.all():
            if u.pk != request.user.pk:
                utils.send_fault_comment_notification(u, f"{request.scheme}://{request.get_host()}", fault, comment)

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
