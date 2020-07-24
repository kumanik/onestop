from django import template
from accounts.models import api_key

register = template.Library()


@register.simple_tag(name='get_key')
def get_key(user):
    try:
        key = api_key.objects.get(user=user)
    except:
        key = None
    return key.apiKey
