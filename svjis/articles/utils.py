import logging
import re
import secrets
import string
import os.path
from . import views, views_contact, views_personal_settings, views_redaction, views_faults, views_adverts, views_admin, models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.hashers import make_password
from openpyxl.styles import NamedStyle, Font, Border, Side, PatternFill


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
    if user.has_perm('articles.svjis_view_fault_menu'):
            result.append({'description': _("Fault reporting"), 'link': reverse(views_faults.faults_list_view) + '?scope=open', 'active': True if active_item == 'faults' else False})
    if user.has_perm('articles.svjis_view_adverts_menu'):
            result.append({'description': _("Adverts"), 'link': reverse(views_adverts.adverts_list_view)  + '?scope=all', 'active': True if active_item == 'adverts' else False})
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


def get_worksheet_header_style():
    header_st = NamedStyle(name="highlight")
    header_st.font = Font(bold=True)
    bd = Side(style='thick', color="000000")
    header_st.border = Border(bottom=bd)
    header_st.fill = PatternFill("solid", fgColor="DDDDDD")
    return header_st


def adjust_worksheet_columns_width(ws, max_width=1000):
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                logger.error("Error: Unable to get cell value length")
        adjusted_width = (max_length + 2) * 1.2
        if adjusted_width > max_width:
             adjusted_width = max_width
        ws.column_dimensions[column_letter].width = adjusted_width


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


def get_template(template_key):
    template = models.Preferences.objects.get(key=template_key)
    if template == None:
        logger.error(f"Error: Missing template {template_key}")
    return template


def send_new_password(user):
    template = get_template('mail.template.lost.password')
    if template is None:
        return
    password = generate_password(6)
    user.password = make_password(password)
    user.save()
    msg = f"Username: {user.username}<br>Password: {password}<br>"
    subj = models.Company.objects.get(pk=1).name
    send_mails(
        [user.email],
        f'{subj} - {_("Credentials")}',
        template.value.format(msg),
        False)


def send_article_notification(user_list, host, article):
    template = get_template('mail.template.article.notification')
    if template is None:
        return
    subj = models.Company.objects.get(pk=1).name
    link = f"<a href='{host}/article/{article.slug}/'>{article.header}</a>"
    send_mails(
        [user.email for user in user_list if user.is_active and user.email != ''],
        f'{subj} - {article.header}',
        template.value.format(link),
        False)


def send_article_comment_notification(user_list, host, article, comment):
    template = get_template('mail.template.comment.notification')
    if template is None:
        return
    subj = models.Company.objects.get(pk=1).name
    link = f"<a href='{host}/article/{article.slug}/'>{article.header}</a>"
    send_mails(
        [user.email for user in user_list if user.is_active and user.email != ''],
        f'{subj} - {article.header}',
        template.value.format(
            f"{comment.author.first_name} {comment.author.last_name}",
            link,
            comment.body.replace('\n', '<br>')),
        False)


def send_new_fault_notification(user_list, host, fault_report):
    template = get_template('mail.template.fault.notification')
    if template is None:
        return
    subj = models.Company.objects.get(pk=1).name
    link = f"<a href='{host}/fault/{fault_report.slug}/'>{fault_report.subject}</a>"
    send_mails(
        [user.email for user in user_list if user.is_active and user.email != ''],
        f'{subj} - {fault_report.subject}',
        template.value.format(
            f"{fault_report.created_by_user.first_name} {fault_report.created_by_user.last_name}",
            link,
            fault_report.description.replace('\n', '<br>')),
        False)


def send_fault_comment_notification(user_list, host, fault_report, comment):
    template = get_template('mail.template.fault.comment.notification')
    if template is None:
        return
    subj = models.Company.objects.get(pk=1).name
    link = f"<a href='{host}/fault/{fault_report.slug}/'>{fault_report.subject}</a>"
    send_mails(
        [user.email for user in user_list if user.is_active and user.email != ''],
        f'{subj} - {fault_report.subject}',
        template.value.format(
            f"{comment.author.first_name} {comment.author.last_name}",
            link,
            comment.body.replace('\n', '<br>')),
        False)


def send_fault_assigned_notification(user, who_assigned_you, host, fault_report):
    template = get_template('mail.template.fault.assigned')
    if template is None:
        return
    subj = models.Company.objects.get(pk=1).name
    link = f"<a href='{host}/fault/{fault_report.slug}/'>{fault_report.subject}</a>"
    send_mails(
        [user.email],
        f'{subj} - {fault_report.subject}',
        template.value.format(
            f"{who_assigned_you.first_name} {who_assigned_you.last_name}",
            link,
            fault_report.description.replace('\n', '<br>')),
        False)


def send_fault_closed_notification(user_list, who_closed, host, fault_report):
    template = get_template('mail.template.fault.closed')
    if template is None:
        return
    subj = models.Company.objects.get(pk=1).name
    link = f"<a href='{host}/fault/{fault_report.slug}/'>{fault_report.subject}</a>"
    send_mails(
        [user.email for user in user_list if user.is_active and user.email != ''],
        f'{subj} - {fault_report.subject}',
        template.value.format(
            f"{who_closed.first_name} {who_closed.last_name}",
            link,
            fault_report.description.replace('\n', '<br>')),
        False)


def send_fault_reopened_notification(user_list, who_closed, host, fault_report):
    template = get_template('mail.template.fault.reopened')
    if template is None:
        return
    subj = models.Company.objects.get(pk=1).name
    link = f"<a href='{host}/fault/{fault_report.slug}/'>{fault_report.subject}</a>"
    send_mails(
        [user.email for user in user_list if user.is_active and user.email != ''],
        f'{subj} - {fault_report.subject}',
        template.value.format(
            f"{who_closed.first_name} {who_closed.last_name}",
            link,
            fault_report.description.replace('\n', '<br>')),
        False)
