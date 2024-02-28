from . import views, models
from django.urls import reverse


def get_tray_menu(view):
    path = reverse(view)
    result = []
    result.append({'description': 'Články', 'link': reverse(views.main_view), 'active': True if path == '/' else False})
    result.append({'description': 'Redakce', 'link': reverse(views.redaction_view), 'active': True if path.startswith('/redaction') else False})
    return  result


def get_aside_menu(view):
    path = reverse(view)
    result = []

    if path == '/':
        result.append({'description': 'Všechy články', 'link': reverse(views.main_view), 'active': True})
        menu_items = models.ArticleMenu.objects.filter(hide=False).all()
        for obj in menu_items:
            result.append({'description': obj.description, 'link': reverse(views.main_view), 'active': False})


    if path.startswith('/redaction'):
        result.append({'description': 'Články', 'link': reverse(views.redaction_view), 'active': True if path == reverse(views.redaction_view) else False})
        result.append({'description': 'Menu', 'link': reverse(views.redaction_menu_view), 'active': True if path.startswith('/redaction_menu') else False})

    return result
