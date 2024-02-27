from . import views
from django.urls import reverse


def get_tray_menu(view):
    path = reverse(view)
    result = []
    result.append({'description': 'Články', 'link': reverse(views.main_view), 'active': True if path == '/' else False})
    result.append({'description': 'Redakce', 'link': reverse(views.redaction_view), 'active': True if path.startswith('/redaction') else False})
    return  result
