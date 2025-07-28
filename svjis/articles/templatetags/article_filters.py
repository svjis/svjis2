from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as gt
from django.conf import settings
import re
from re import IGNORECASE, compile

register = template.Library()


@register.filter()
def highlight(text, search):
    if search == '':
        return text
    rgx = compile(f'({search})(?![^<>]*>)', IGNORECASE)
    highlighted = rgx.sub(lambda m: f'<b style="color:black;background-color:#ffff66">{m.group()}</b>', text)
    return mark_safe(highlighted)


@register.filter()
def inject_pictures(text, assets):
    for a in assets:
        file = a['asset'].file
        basename = a['basename']
        text = text.replace('{' + basename + '}', f'<img class="article-img" src="/media/{file}" alt="{basename}">')
    return mark_safe(text)


@register.filter()
def replace_url_to_link(value):
    # Replace url to link
    urls = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE | re.UNICODE)
    value = urls.sub(r'<a href="\1" target="_blank">\1</a>', value)
    # Replace email to mailto
    urls = re.compile(r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)", re.MULTILINE | re.UNICODE)
    value = urls.sub(r'<a href="mailto:\1">\1</a>', value)
    return mark_safe(value)


@register.filter()
def yes_no(bool_value):
    result = gt("Yes") if bool_value else gt("No")
    return mark_safe(result)


# settings value
@register.simple_tag
def settings_value(name):
    return mark_safe(getattr(settings, name, ""))


@register.simple_tag
def get_languages():
    return settings.LANGUAGES
