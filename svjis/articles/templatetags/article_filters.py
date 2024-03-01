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


@register.filter(name='highlight')
def highlight(text, search):
    if search == '':
        return text
    rgx = compile(rescape(search), IGNORECASE)
    highlighted = rgx.sub(
            lambda m: '<b style="color:black;background-color:#ffff66">{}</b>'.format(m.group()),
            text
        )
    # highlighted = text.replace(search, '<b style="color:black;background-color:#ffff66">{}</b>'.format(search))
    return mark_safe(highlighted)

# settings value
@register.simple_tag
def settings_value(name):
    return mark_safe(getattr(settings, name, ""))
