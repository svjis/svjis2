import logging
import re
import secrets
import string
from . import views, views_personal_settings, views_redaction, views_admin, models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.hashers import make_password


logger = logging.getLogger(__name__)


def get_tray_menu(active_item: str, user) -> list:
    result = []
    result.append({'description': _("Articles"), 'link': reverse(views.main_view), 'active': True if active_item == 'articles' else False})
    if user.has_perm('articles.svjis_view_personal_menu'):
            result.append({'description': _("Personal settings"), 'link': reverse(views_personal_settings.personal_settings_edit_view), 'active': True if active_item == 'personal_settings' else False})
    if user.has_perm('articles.svjis_view_redaction_menu'):
            result.append({'description': _("Redaction"), 'link': reverse(views_redaction.redaction_article_view), 'active': True if active_item == 'redaction' else False})
    if user.has_perm('articles.svjis_view_admin_menu'):
            result.append({'description': _("Administration"), 'link': reverse(views_admin.admin_company_edit_view), 'active': True if active_item == 'admin' else False})
    return  result


def generate_password(len: int) -> str:
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(len))
    return password


def validate_email_address(email_address: str) -> bool:
    return re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email_address) != None


def send_mails(recipient_list: list, subject: str, html_body: str, immediately: bool) -> None:
    if settings.EMAIL_HOST == '':
         logger.error("Error: It seems E-Mail system is not configured yet.")
         return

    if immediately:
          message = EmailMessage(subject, html_body, settings.EMAIL_HOST_USER, recipient_list)
          message.content_subtype = 'html'
          message.send()
    else:
          for r in recipient_list:
            if not validate_email_address(r):
                  logger.warning(f"It seems E-Mail address is not valid: {r} - skipping it")
            else:
                models.MessageQueue.objects.create(email=r, subject=subject, body=html_body, status=0)


def send_new_password(user):
    template_key = 'mail.template.lost.password'
    template = models.Preferences.objects.get(key=template_key)
    if template == None:
        logger.error(f"Error: Missing template {template_key}")
        return
    password = generate_password(6)
    user.password = make_password(password)
    user.save()
    msg = f"Username: {user.username}<br>Password: {password}<br>"
    send_mails([user.email], "Lost password", template.value.format(msg), False)
