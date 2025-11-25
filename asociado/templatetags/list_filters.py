from django import template

register = template.Library()


@register.filter
def not_in(value, excluded_list):
    excluded = [int(x) for x in excluded_list.split(",")]
    return int(value) not in excluded
