from . import views, models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def get_tray_menu(view, user):
    path = reverse(view)
    result = []
    result.append({'description': _("Articles"), 'link': reverse(views.main_view), 'active': True if path == '/' else False})
    if user.is_active:
            result.append({'description': _("Redaction"), 'link': reverse(views.redaction_article_view), 'active': True if path.startswith('/redaction') else False})
            result.append({'description': _("Administration"), 'link': reverse(views.admin_user_view), 'active': True if path.startswith('/admin') else False})
    return  result


def get_aside_menu(view, ctx):
    path = reverse(view)
    result = []

    if path == '/':
        header = ctx.get('header', None)
        result.append({'description': _("All articles"), 'link': reverse(views.main_view), 'active': True if header == _("All articles") else False})
        menu_items = models.ArticleMenu.objects.filter(hide=False).all()
        for obj in menu_items:
            result.append({'description': obj.description, 'link': reverse('main_filtered', kwargs={'menu':obj.id}), 'active': True if header == obj.description else False})


    if path.startswith('/redaction'):
        result.append({'description': _("Articles"), 'link': reverse(views.redaction_article_view), 'active': True if path == reverse(views.redaction_article_view) else False})
        result.append({'description': _("Menu"), 'link': reverse(views.redaction_menu_view), 'active': True if path.startswith('/redaction_menu') else False})


    if path.startswith('/admin'):
        result.append({'description': _("Users"), 'link': reverse(views.admin_user_view), 'active': True if path == reverse(views.admin_user_view) else False})


    return result
