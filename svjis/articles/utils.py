from . import views, views_redaction, views_admin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def get_tray_menu(active_item, user):
    result = []
    result.append({'description': _("Articles"), 'link': reverse(views.main_view), 'active': True if active_item == 'articles' else False})
    if user.is_staff:
            result.append({'description': _("Redaction"), 'link': reverse(views_redaction.redaction_article_view), 'active': True if active_item == 'redaction' else False})
    if user.is_superuser:
            result.append({'description': _("Administration"), 'link': reverse(views_admin.admin_user_view), 'active': True if active_item == 'admin' else False})
    return  result
