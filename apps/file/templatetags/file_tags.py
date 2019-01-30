from django import template
from ..server import *
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def fetch_tags():
    result_db = tag_db.query_tag_list()
    return result_db