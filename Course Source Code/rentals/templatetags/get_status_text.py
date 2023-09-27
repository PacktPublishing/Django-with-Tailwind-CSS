from django import template
from ..choices import STATUS_CHOICES

register = template.Library()

@register.filter
def get_status_text(value):
    if not value: return
    data = dict(STATUS_CHOICES)
    return data[value]