from django import template
# import meters.views as views
# from meters.mode ls import Address
#from meters.utils import menu

register = template.Library()


# @register.simple_tag(name='getcats')
# def get_categories():
#     return views.cats_db

# @register.simple_tag
# def get_menu():
#     return menu

@register.inclusion_tag('meters/show_menu.html')
def show_menu( menu, address_slug, user ):
    return { 'menu': menu, 'address_slug':address_slug, 'user_id':user }

# @register.inclusion_tag('meters/choice_address.html')
# def show_address( form ):
#     return { 'form_address': form }

# @register.inclusion_tag('meters/choice_address.html')
# def show_address( vib_id=0 ):
#     addr = Address.objects.all()
#     return { 'addr': addr, 'vib_id': vib_id }