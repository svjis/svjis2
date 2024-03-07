from . import views, views_personal_settings, views_redaction, views_admin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def get_tray_menu(active_item, user):
    result = []
    result.append({'description': _("Articles"), 'link': reverse(views.main_view), 'active': True if active_item == 'articles' else False})
    if user.has_perm('articles.svjis_view_personal_menu'):
            result.append({'description': _("Personal settings"), 'link': reverse(views_personal_settings.personal_settings_edit_view), 'active': True if active_item == 'personal_settings' else False})
    if user.has_perm('articles.svjis_view_redaction_menu'):
            result.append({'description': _("Redaction"), 'link': reverse(views_redaction.redaction_article_view), 'active': True if active_item == 'redaction' else False})
    if user.has_perm('articles.svjis_view_admin_menu'):
            result.append({'description': _("Administration"), 'link': reverse(views_admin.admin_user_view), 'active': True if active_item == 'admin' else False})
    return  result
