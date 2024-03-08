from . import utils, forms, models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST


def get_side_menu(active_item, user):
    result = []
    if user.has_perm('articles.svjis_edit_admin_users'):
        result.append({'description': _("Users"), 'link': reverse(admin_user_view), 'active': True if active_item == 'users' else False})
    if user.has_perm('articles.svjis_edit_admin_groups'):
        result.append({'description': _("Groups"), 'link': reverse(admin_group_view), 'active': True if active_item == 'groups' else False})
    if user.has_perm('articles.svjis_edit_admin_properties'):
        result.append({'description': _("Properties"), 'link': reverse(admin_property_view), 'active': True if active_item == 'properties' else False})
    if user.has_perm('articles.svjis_view_admin_menu'):
        result.append({'description': _("Waiting messages"), 'link': reverse(admin_messages_view), 'active': True if active_item == 'messages' else False})
    return result


# Administration - User
@permission_required("articles.svjis_edit_admin_users")
@require_GET
def admin_user_view(request):
    user_list = User.objects.all()
    ctx = {
        'aside_menu_name': _("Administration"),
    }
    ctx['aside_menu_items'] = get_side_menu('users', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('admin', request.user)
    ctx['object_list'] = user_list
    return render(request, "admin_user.html", ctx)


@permission_required("articles.svjis_edit_admin_users")
@require_GET
def admin_user_edit_view(request, pk):
    if pk != 0:
        user_i = get_object_or_404(User, pk=pk)
        profile_i, created = models.UserProfile.objects.get_or_create(user=user_i)
    else:
        user_i = User
        profile_i = models.UserProfile

    group_list = []
    user_group_list = []
    if pk != 0:
        user_group_list = Group.objects.filter(user__id=user_i.id)
    for g in Group.objects.all():
        item = {'name': g.name, 'checked': g in user_group_list}
        group_list.append(item)

    ctx = {
        'aside_menu_name': _("Administration"),
    }
    ctx['user_i'] = user_i
    ctx['profile_i'] = profile_i
    ctx['group_list'] = group_list
    ctx['pk'] = pk
    ctx['aside_menu_items'] = get_side_menu('users', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('admin', request.user)
    return render(request, "admin_user_edit.html", ctx)


@permission_required("articles.svjis_edit_admin_users")
@require_POST
def admin_user_save_view(request):
    pk = int(request.POST['pk'])
    if pk != 0:
        user_i = get_object_or_404(User, pk=pk)
        user_form = forms.UserForm(request.POST, instance=user_i)
        user_profile_form = forms.UserProfileForm(request.POST, instance=user_i.userprofile)
    else:
        user_form = forms.UserForm(request.POST)
        user_profile_form = forms.UserProfileForm(request.POST)

    if user_form.is_valid() and user_profile_form.is_valid():
        u = user_form.save()
        u.userprofile = user_profile_form.instance
        u.userprofile.save()

        password = request.POST.get('password', '')
        if password != '':
            u.password = make_password(password)
            u.save()

        # Set groups
        user_group_list = Group.objects.filter(user__id=u.id)
        for g in Group.objects.all():
            group_set = request.POST.get(g.name, False) == 'on'
            if group_set and g not in user_group_list:
                u.groups.add(g)
            if not group_set and g in user_group_list:
                u.groups.remove(g)

    else:
        for error in user_form.errors:
            messages.error(request, f"{_('Form validation error')}: {error}")
        for error in user_profile_form.errors:
            messages.error(request, f"{_('Form validation error')}: {error}")
        return redirect(reverse('admin_user_edit', kwargs={'pk':pk}))

    return redirect(admin_user_view)


# Administration - Group
@permission_required("articles.svjis_edit_admin_groups")
@require_GET
def admin_group_view(request):
    group_list = Group.objects.all()
    ctx = {
        'aside_menu_name': _("Administration"),
    }
    ctx['aside_menu_items'] = get_side_menu('groups', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('admin', request.user)
    ctx['object_list'] = group_list
    return render(request, "admin_group.html", ctx)


@permission_required("articles.svjis_edit_admin_groups")
@require_GET
def admin_group_edit_view(request, pk):
    if pk != 0:
        i = get_object_or_404(Group, pk=pk)
        form = forms.GroupEditForm(instance=i)
    else:
        i = Group
        form = forms.GroupEditForm

    permission_list = []
    group_perm_list = []
    if pk != 0:
        group_perm_list = Permission.objects.filter(group__id=i.id)
    for p in Permission.objects.all():
        if p.codename.startswith('svjis_'):
            item = {'name': p.codename, 'checked': p in group_perm_list}
            permission_list.append(item)

    ctx = {
        'aside_menu_name': _("Administration"),
    }
    ctx['form'] = form
    ctx['instance'] = i
    ctx['permission_list'] = permission_list
    ctx['pk'] = pk
    ctx['aside_menu_items'] = get_side_menu('groups', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('admin', request.user)
    return render(request, "admin_group_edit.html", ctx)


@permission_required("articles.svjis_edit_admin_groups")
@require_POST
def admin_group_save_view(request):
    pk = int(request.POST['pk'])
    if pk == 0:
        form = forms.GroupEditForm(request.POST)
    else:
        instance = get_object_or_404(Group, pk=pk)
        form = forms.GroupEditForm(request.POST, instance=instance)
    if form.is_valid:
        instance = form.save()

        # Set permissions
        group_perm_list = Permission.objects.filter(group__id=instance.id)
        for p in Permission.objects.all():
            if p.codename.startswith('svjis_'):
                perm_set = request.POST.get(p.codename, False) == 'on'
                if perm_set and p not in group_perm_list:
                    instance.permissions.add(p)
                if not perm_set and p in group_perm_list:
                    instance.permissions.remove(p)
    else:
        for error in form.errors:
            messages.error(request, f"{_('Form validation error')}: {error}")

    return redirect(admin_group_view)


@permission_required("articles.svjis_edit_admin_groups")
@require_GET
def admin_group_delete_view(request, pk):
    obj = get_object_or_404(Group, pk=pk)
    obj.delete()
    return redirect(admin_group_view)


# Administration - Properties
@permission_required("articles.svjis_edit_admin_properties")
@require_GET
def admin_property_view(request):
    property_list = models.ApplicationSetup.objects.all()
    ctx = {
        'aside_menu_name': _("Administration"),
    }
    ctx['aside_menu_items'] = get_side_menu('properties', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('admin', request.user)
    ctx['object_list'] = property_list
    return render(request, "admin_property.html", ctx)


@permission_required("articles.svjis_edit_admin_properties")
@require_GET
def admin_property_edit_view(request, pk):
    if pk != 0:
        i = get_object_or_404(models.ApplicationSetup, pk=pk)
        form = forms.ApplicationSetupForm(instance=i)
    else:
        form = forms.ApplicationSetupForm

    ctx = {
        'aside_menu_name': _("Administration"),
    }
    ctx['form'] = form
    ctx['pk'] = pk
    ctx['aside_menu_items'] = get_side_menu('properties', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('admin', request.user)
    return render(request, "admin_property_edit.html", ctx)


@permission_required("articles.svjis_edit_admin_properties")
@require_POST
def admin_property_save_view(request):
    pk = int(request.POST['pk'])
    if pk == 0:
        form = forms.ApplicationSetupForm(request.POST)
    else:
        instance = get_object_or_404(models.ApplicationSetup , pk=pk)
        form = forms.ApplicationSetupForm(request.POST, instance=instance)
    if form.is_valid:
        form.save()
    else:
        for error in form.errors:
            messages.error(request, f"{_('Form validation error')}: {error}")
    return redirect(admin_property_view)


@permission_required("articles.svjis_edit_admin_properties")
@require_GET
def admin_property_delete_view(request, pk):
    obj = get_object_or_404(models.ApplicationSetup, pk=pk)
    obj.delete()
    return redirect(admin_property_view)


# Administration - Waiting messages
@permission_required("articles.svjis_view_admin_menu")
@require_GET
def admin_messages_view(request):
    message_list = models.MessageQueue.objects.filter(status=0)
    ctx = {
        'aside_menu_name': _("Administration"),
    }
    ctx['aside_menu_items'] = get_side_menu('messages', request.user)
    ctx['tray_menu_items'] = utils.get_tray_menu('admin', request.user)
    ctx['object_list'] = message_list
    return render(request, "admin_messages.html", ctx)
