from django import template


register = template.Library()

@register.filter
def can_be_managed(appointment, user):
    return appointment.can_be_managed_by(user)