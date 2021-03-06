from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime, timedelta
register = template.Library()


@register.filter(expects_localtime=True, is_safe=False)
def get_birthday(value, arg=None):
    """
     A simple template tag to take in the number of days
     until the users next birthday and convert that into
     a neatly formatted date.
    """

    if value:
        return "{:%d, %b %Y}".format(datetime.now() + timedelta(days=value))
    return ''
