from django import template


register = template.Library()


@register.inclusion_tag('blog/tags/form_field_errors.html')
def show_form_errors(field_errors, block_class=None):
    return {
        'errors': field_errors,
        'block': block_class,
    }


@register.inclusion_tag('blog/tags/form_field_errors.html')
def form_errors(form, block_class=None):
    return {
        'errors': form.non_field_errors,
        'block': block_class,
    }


@register.inclusion_tag('blog/tags/messages.html', takes_context=True)
def show_messages(context, show=True):
    return {'messages': (context.get('messages') if show else None)}
