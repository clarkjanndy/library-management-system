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
    
@register.filter()
def abbreviate(value):
    if value == 'Bachelor of Science in Information Technology':
        return 'BSIT'
    elif value == 'Bachelor of Science in Hospitality Management':
        return 'BSHM'
    elif value == 'Bachelor of Science in Criminology':
        return 'BSCrim'
    elif value == 'Bachelor of Secondary Education':
        return 'BSEd'
    elif value == 'Bachelor of Elementary Education':
        return 'BEEd'
    else:
        return 'TBA'
