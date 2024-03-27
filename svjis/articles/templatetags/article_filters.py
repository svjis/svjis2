from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.conf import settings
import markdown as md
from re import IGNORECASE, compile, escape as rescape

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.filter()
def highlight(text, search):
    if search == '':
        return text
    rgx = compile(rescape(search), IGNORECASE)
    highlighted = rgx.sub(
            lambda m: '<b style="color:black;background-color:#ffff66">{}</b>'.format(m.group()),
            text
        )
    return mark_safe(highlighted)


@register.filter()
def inject_pictures(text, assets):
    for a in assets:
        file = a['asset'].file
        text = text.replace('{' + a['basename'] + '}', f'<img src="/media/{file}" alt="{a['basename']}">')
    return mark_safe(text)


# settings value
@register.simple_tag
def settings_value(name):
    return mark_safe(getattr(settings, name, ""))
