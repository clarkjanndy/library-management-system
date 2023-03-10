from django import template

register = template.Library()


@register.filter()
def cardinal(value):
    if value == 1:
        return '1st'
    elif value == 2:
        return '2nd'
    elif value == 3:
        return '3rd'
    else:
        return f"{value}th"
