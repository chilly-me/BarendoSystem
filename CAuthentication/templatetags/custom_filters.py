from django import template

register = template.Library()


@register.filter
def format_number(value):
    try:
        # Format the number with commas for thousands and preserve decimals
        return f"{value:,.2f}"
    except (TypeError, ValueError):
        return value
