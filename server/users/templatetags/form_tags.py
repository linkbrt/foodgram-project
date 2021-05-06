from django import template


register = template.Library()


@register.filter
def prettify_help_text(help_text: str):
    if not help_text:
        return ''

    help_text = help_text.replace('<ul>', '').replace('</ul>', '')
    result = []
    for item in help_text.split('<li>'):
        result.append(item.replace('</li>', ''))

    return result