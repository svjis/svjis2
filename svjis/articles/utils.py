import logging
import re
import secrets
import string
import os.path
from . import views, views_contact, views_personal_settings, views_redaction, views_admin, models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.template.defaultfilters import slugify



logger = logging.getLogger(__name__)


def get_context():
     ctx = {}
     company, _created = models.Company.objects.get_or_create(pk=1)
     if company is not None:
          ctx['company_picture'] = company.header_picture
          ctx['company_name'] = company.name
          ctx['web_title'] = company.name
     return ctx


def get_tray_menu(active_item: str, user) -> list:
    result = []
    result.append({'description': _("Articles"), 'link': reverse(views.main_view), 'active': True if active_item == 'articles' else False})
    result.append({'description': _("Contact"), 'link': reverse(views_contact.contact_view), 'active': True if active_item == 'contact' else False})
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


def wrap_assets(assets):
    supported_icons = ['doc', 'docx', 'gif', 'htm', 'html', 'jpeg', 'jpg', 'pdf', 'pps', 'txt', 'xls', 'xlsx', 'zip']
    result = []
    for a in assets:
        item = {}
        item['asset'] = a
        basename = os.path.basename(a.file.path)
        _file_name, file_extension = os.path.splitext(basename)
        file_extension = file_extension[1:]
        item['basename'] = basename
        if file_extension.lower() in supported_icons:
            item['icon'] = f'Files_{file_extension.lower()}.gif'
        else:
            item['icon'] = 'Files_unknown.gif'
        result.append(item)
    return result


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


def send_message_queue():
     messages = models.MessageQueue.objects.filter(status=0)
     for m in messages:
          send_mails([m.email], m.subject, m.body, True)
          m.status = 1
          m.save()


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
    subj = models.Company.objects.get(pk=1).name
    send_mails([user.email], f'{subj} - {_("Credentials")}', template.value.format(msg), False)


def send_article_notification(user, host, article):
    template_key = 'mail.template.article.notification'
    template = models.Preferences.objects.get(key=template_key)
    if template == None:
        logger.error(f"Error: Missing template {template_key}")
        return

    subj = models.Company.objects.get(pk=1).name
    link = f"<a href='{host}/article/{article.pk}/'>{article.header}</a>"
    send_mails([user.email], f'{subj} - {article.header}', template.value.format(link), False)


def send_article_comment_notification(user, host, article, comment):
    template_key = 'mail.template.comment.notification'
    template = models.Preferences.objects.get(key=template_key)
    if template == None:
        logger.error(f"Error: Missing template {template_key}")
        return

    subj = models.Company.objects.get(pk=1).name
    link = f"<a href='{host}/article/{article.pk}/'>{article.header}</a>"
    send_mails([user.email], f'{subj} - {article.header}', template.value.format(f"{comment.author.first_name} {comment.author.last_name}", link, comment.body), False)


def unique_slugify(instance, value, slug_field_name='slug', queryset=None, slug_separator='-'):
    """
    From: https://djangosnippets.org/snippets/690/
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value
