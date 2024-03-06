from . import utils, forms, models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


def get_side_menu(active_item, user):
    result = []
    if user.has_perm('articles.svjis_edit_admin_users'):
        result.append({'description': _("Users"), 'link': reverse(admin_user_view), 'active': True if active_item == 'users' else False})
    if user.has_perm('articles.svjis_edit_admin_groups'):
        result.append({'description': _("Groups"), 'link': reverse(admin_group_view), 'active': True if active_item == 'groups' else False})
    return result


# Administration - User
@permission_required("articles.svjis_edit_admin_users")
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
def admin_user_save_view(request):
    if request.method == "POST":
        pk = int(request.POST['pk'])
        if pk != 0:
            user_i = get_object_or_404(User, pk=pk)
            profile_i, created = models.UserProfile.objects.get_or_create(user=user_i)
        else:
            user_i = User.objects.create(
                            username=request.POST.get('username', ''),
                            password=make_password(request.POST.get('password', '')))
            profile_i = models.UserProfile.objects.create(user=user_i)

        profile_i.salutation = request.POST.get('salutation', '')
        user_i.first_name = request.POST.get('firstName', '')
        user_i.last_name = request.POST.get('lastName', '')
        profile_i.internal_note = request.POST.get('internalNote', '')
        profile_i.address = request.POST.get('address', '')
        profile_i.city = request.POST.get('city', '')
        profile_i.post_code = request.POST.get('postCode', '')
        profile_i.country = request.POST.get('country', '')
        profile_i.phone = request.POST.get('phone', '')
        user_i.email = request.POST.get('email', '')
        profile_i.show_in_phonelist = request.POST.get('phoneList', False) == 'on'
        password = request.POST.get('password', '')
        user_i.is_active = request.POST.get('active', False) == 'on'

        if password != '':
            user_i.password = make_password(password)

        user_i.save()
        profile_i.save()

        # Set groups
        user_group_list = Group.objects.filter(user__id=user_i.id)
        for g in Group.objects.all():
            group_set = request.POST.get(g.name, False) == 'on'
            if group_set and g not in user_group_list:
                user_i.groups.add(g)
            if not group_set and g in user_group_list:
                user_i.groups.remove(g)

    return redirect(admin_user_view)


# Administration - Group
@permission_required("articles.svjis_edit_admin_groups")
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
def admin_group_save_view(request):
    if request.method == "POST":
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
            messages.error(request, _("Invalid form input"))

    return redirect(admin_group_view)


@permission_required("articles.svjis_edit_admin_groups")
def admin_group_delete_view(request, pk):
    obj = get_object_or_404(Group, pk=pk)
    obj.delete()
    return redirect(admin_group_view)
