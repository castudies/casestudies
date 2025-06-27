from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    """Add CSS class to a form field widget."""
    try:
        if hasattr(field, 'as_widget'):
            return field.as_widget(attrs={**field.field.widget.attrs, 'class': css})
        else:
            # If it's not a proper form field, return as is
            return field
    except Exception:
        # If there's any error, return the field as is
        return field 