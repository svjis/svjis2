from . import views, models
from django.urls import reverse


def get_tray_menu(view):
    path = reverse(view)
    result = []
    result.append({'description': 'Články', 'link': reverse(views.main_view), 'active': True if path == '/' else False})
    result.append({'description': 'Redakce', 'link': reverse(views.redaction_article_view), 'active': True if path.startswith('/redaction') else False})
    return  result


def get_aside_menu(view, ctx):
    path = reverse(view)
    result = []

    if path == '/':
        header = ctx.get('header', None)
        result.append({'description': 'Všechny články', 'link': reverse(views.main_view), 'active': True if header == 'Všechny články' else False})
        menu_items = models.ArticleMenu.objects.filter(hide=False).all()
        for obj in menu_items:
            result.append({'description': obj.description, 'link': reverse('main_filtered', kwargs={'menu':obj.id}), 'active': True if header == obj.description else False})


    if path.startswith('/redaction'):
        result.append({'description': 'Články', 'link': reverse(views.redaction_article_view), 'active': True if path == reverse(views.redaction_article_view) else False})
        result.append({'description': 'Menu', 'link': reverse(views.redaction_menu_view), 'active': True if path.startswith('/redaction_menu') else False})

    return result
