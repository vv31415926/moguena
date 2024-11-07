from datetime import date
import threading

#from .forms import VibAddressForm, AddElectroForm, AddWaterForm, ItemElectroForm, ItemWaterForm
from .models import Address, Electro, Water
from django.core.cache import cache

class SingletonCache:
    @staticmethod
    def get_address():
        address = cache.get('address')
        if address is None:
            address = {'id':None,'slug':None,'name':None}
            cache.set('address', address, timeout=None)
        return address

    @staticmethod
    def set_address(id=None, slug = None, name = None):
        address = {'id': id, 'slug': slug, 'name': name}
        cache.set('address', address, timeout=None)

    @staticmethod
    def get_tarif():
        tarif = cache.get('tarif')
        if tarif is None:
            tarif = {'id': None, 'slug': None, 'name': None, 'number':0}
            cache.set('tarif', tarif, timeout=None)
        return tarif

    @staticmethod
    def set_tarif(id=None, slug = None, name = None, number=0):
        tarif = {'id': id, 'slug': slug, 'name': name, 'number': number}
        cache.set('tarif', tarif, timeout=None)

    @staticmethod
    def get_menu():
        menu = [
            {'title': "начало", 'url_name': 'meters:home'},
            {'title': "Адрес", 'url_name': 'submenu',
             'submenu': None},
            {'title': "Показания", 'url_name': 'submenu',
             'submenu': [{'title': 'Электричество', 'type': 'meters:electro'},
                         {'title': 'Водоснабжение', 'type': 'meters:water'}]
             },
            {'title': "О сайте", 'url_name': 'meters:about'},
            {'title': "Обратная связь", 'url_name': 'meters:contact'},
        ]
        for mi in menu:
            if mi['url_name'] == 'submenu':
                if mi['title'] == 'Адрес':
                    lst = []
                    a = Address.objects.all()
                    for v in a:
                        lst.append({'title': f'{v.city}, {v.street}', 'id': v.pk, 'slug': v.slug})
                    mi['submenu'] = lst
        return menu


class DataMixin:
    #paginate_by = 5
    title_page = None
    form_address= None
    extra_context = {}

    def __init__(self):
        # self.sel_singleton = SelectionSingleton()
        if self.title_page:
            self.extra_context['title'] = self.title_page
        # if 'menu' not in self.extra_context:  # передается в теге
        #     self.extra_context['menu'] = menu

    def get_mixin_context(self, context={}, **kwargs):
        today = date.today()
        curdate = today.strftime("%Y-%m-%d")
        # HTML5 требует, чтобы значение для поля ввода типа date было в формате YYYY-MM-DD, независимо от формата, который вы используете при передаче даты из Python/Django
        context['curdate'] = curdate
        context['curdatetxt'] = self.ymd2dmy(curdate)

        context['address_id'] = SingletonCache.get_address()['id']  # check_address.address_id
        context['address_slug'] = SingletonCache.get_address()['slug']  # check_address.address_slug
        context['address_name'] = SingletonCache.get_address()['name']  # check_address.address_name
        if SingletonCache.get_tarif()['id']:
            context['tarif_id'] = SingletonCache.get_tarif()['id']  # check_address.tarif_id
        else:
            context['tarif_id'] = SingletonCache.get_tarif()

        if kwargs:
            context.update(kwargs)
        return context

    def ymd2dmy(self, d: str):
        if d.find('.') >= 0:
            lst = d.split('.')[::-1]
        elif d.find('-') >= 0:
            lst = d.split('-')[::-1]
        else:
            lst = d.split('/')[::-1]
        return '.'.join(lst)

    def dmy2ymd(self, sd: str):
        if sd.find('.') >= 0:
            lst = sd.split('.')[::-1]
        elif sd.find('-') >= 0:
            lst = sd.split('-')[::-1]
        else:
            lst = sd.split('/')[::-1]
        return '.'.join(lst)