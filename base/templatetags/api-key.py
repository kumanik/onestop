from django import template
from accounts.models import api_key

register = template.Library()


@register.simple_tag(name='get_key')
def get_key(user):
    key = api_key.objects.get(user=user)
    if key is not None:
        return key.apiKey
