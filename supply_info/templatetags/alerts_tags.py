from django import template

register = template.Library()


@register.filter(name='less_or_equal_bool_to_text')
def less_or_equal_bool_to_text(value):
    if value:
        return 'mniej lub równe:'
    else:
        return 'więcej niż:'
