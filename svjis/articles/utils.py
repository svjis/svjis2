from . import views
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
        result.append({'description': 'Všechny články', 'link': '/', 'active': True})
        result.append({'description': 'Dokumenty', 'link': '/', 'active': False})
        result.append({'description': 'Smlouvy', 'link': '/', 'active': False})

    if path.startswith('/redaction'):
        result.append({'description': 'Články', 'link': '/', 'active': True})

    return result
