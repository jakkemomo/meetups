from django import template

register = template.Library()


def id_is_in(var, args):
    if args is None:
        return False
    return any(list.get('id') == var for list in args)


register.filter('id_is_in', id_is_in)
