from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import F
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date

from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, TemplateView, CreateView, DetailView, UpdateView

from .forms import VibAddressForm, AddElectroForm, AddWaterForm, ItemElectroForm, ItemWaterForm, NewElectroForm, \
    NewWaterForm, AddElectroDaylyForm, ContactForm
from .models import Address, Electro, Water, Tarif
from .utils import DataMixin,  SingletonCache

# today = date.today()  # +timedelta(days=10)
# # Преобразование даты в строку
# curdate = today.strftime("%Y-%m-%d")  # HTML5 требует, чтобы значение для поля ввода типа date было в формате YYYY-MM-DD, независимо от формата, который вы используете при передаче даты из Python/Django
# curdatetxt = utl.ymd2dmy(curdate)

def address( request: HttpRequest, addr_id: int   ):
    address = Address.objects.get( id=addr_id )

    SingletonCache.set_address(id=address.id, slug=address.slug, name=address)
    SingletonCache.set_tarif()

    url = reverse( 'meters:home' )
    return redirect(url)

class MetersHome( DataMixin, TemplateView ):
    template_name = 'meters/index.html'

    extra_context = {
        'title': 'ЖКХ',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #a = self.get_mixin_context(context)
        return self.get_mixin_context(context)

# ------------------------------------------------------------------------------
class ShowElectro(  LoginRequiredMixin, DataMixin, ListView ):
    #model = Electro
    template_name = 'meters/electro.html'
    context_object_name = 'indication'
    #allow_empty = False
    #success_url = reverse_lazy('home')  # URL по умолчанию

    def get_queryset(self):
        address_slug = self.kwargs['addr_slug']
        address = get_object_or_404(Address, slug=address_slug)
        indication = Electro.objects.filter(addr_id=address.pk)

        if indication.exists():
            #SelectionSingleton().set_tarif( id=indication[0].tar_id )
            SingletonCache.set_tarif(id=indication[0].tar_id)
            #check_address.tarif_id = indication[0].tar_id
        else:
            #SelectionSingleton().set_tarif(id=None)
            SingletonCache.set_tarif(id=None)
            #check_address.tarif_id = None
        return indication

    # def queryset(self):
    #     address_slug = self.kwargs['addr_slug']
    #     address = get_object_or_404(Address, slug=address_slug )
    #     indication = Electro.objects.filter(addr_id=address.pk)
    #     if indication.exists:
    #         check_address.tarif_id = indication[0].tar_id
    #     else:
    #         check_address.tarif_id = None
    #     return indication

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_meters'] = 'electro'
        return self.get_mixin_context(context)

# ------------------------------------------------------------------------------
class ItemElectro( DataMixin, UpdateView ):
    #model = Electro
    form_class = ItemElectroForm
    template_name = 'meters/e_indication.html'
    slug_url_kwarg = 'eitem_slug'
    context_object_name = 'indication'
    title_page = 'Просмотр показания'
    success_url = reverse_lazy('meters:electro')  # URL по умолчанию

    def form_valid(self, form):
        c = self.get_mixin_context()
        address_slug = c['address_slug']
        form.save()
        url = reverse('meters:electro', kwargs={'addr_slug': address_slug })
        return redirect(url)
        #return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # c = self.get_mixin_context()
        # address_name = c['address_name']
        context = super().get_context_data(**kwargs)
        a = self.get_mixin_context(context)
        return self.get_mixin_context(context)

    def get_object(self, queryset=None):
        return get_object_or_404( Electro, slug=self.kwargs[self.slug_url_kwarg] )

# ------------------------------------------------------------------------------
class ShowWater( LoginRequiredMixin, DataMixin, ListView ):
    template_name = 'meters/water.html'
    context_object_name = 'indication'
    allow_empty = False
    #success_url = reverse_lazy('home')  # URL по умолчанию

    def queryset(self):
        address_slug = self.kwargs['addr_slug']
        address = get_object_or_404(Address, slug=address_slug )
        indication = Water.objects.filter( addr_id=address.pk )
        return indication

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_meters'] = 'Водоснабжение'
        return self.get_mixin_context(context)
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
class ItemWater( DataMixin, UpdateView ):
    #model = Electro
    form_class = ItemWaterForm
    template_name = 'meters/w_indication.html'
    slug_url_kwarg = 'witem_slug'
    context_object_name = 'indication'
    title_page = 'Просмотр показания'
    success_url = reverse_lazy('meters:water')  # URL по умолчанию

    def form_valid(self, form):
        c = self.get_mixin_context()
        address_slug = c['address_slug']
        form.save()
        url = reverse('meters:water', kwargs={'addr_slug': address_slug })
        return redirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

    def get_object(self, queryset=None):
        return get_object_or_404( Water, slug=self.kwargs[self.slug_url_kwarg] )

# ---------------------------------------------------------------------------------------------
class SelectorService(View):
    a=1
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_meters'] = 'electro'
        return self.get_mixin_context(context)
    def get(self, request, type_meters, addr_slug):
        # Получаем значение параметра addr_slug
        type_meters = self.kwargs.get('type_meters')
        addr_slug = self.kwargs.get('addr_slug')
        if type_meters == "electro":
            # url = reverse( 'add_electro', kwargs={'e_slug': 'electro'})
            url = reverse('meters:add_electro')
        else:
            url = reverse('meters:add_water')
        return redirect(url)

#----------------------------------------------------------------------------------------------
class AddElectro( DataMixin, CreateView  ):
    model = Electro
    form_class = AddElectroForm
    template_name = 'meters/add_electro.html'
    title_page = 'Добавление показания'
    success_url = reverse_lazy('meters:electro')  # URL по умолчанию

    def form_valid(self, form):
        c = self.get_mixin_context()
        tarif_id = c['tarif_id']
        address_id = c['address_id']
        # Получаем объект без сохранения его в базу данных
        instance  = form.save(commit=False)
        f = form.cleaned_data
        dr = f['date_reading']  # дата занесения для слага
        address_slug = self.kwargs['address_slug']
        instance.slug = f'{address_slug}-{dr.strftime("%Y-%m")}'
        instance.tar = Tarif.objects.get(id=tarif_id)
        instance.addr_id = address_id

        instance.author = self.request.user

        instance.save()

        url = reverse( 'meters:electro', kwargs={'addr_slug': address_slug})
        return redirect( url )
        #return super().form_valid(form)


    def get_context_data(self, **kwargs):
        # c = self.get_mixin_context()
        # address_name = c['address_name']
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

class AddElectroDayly( DataMixin, CreateView  ):
    model = Electro
    form_class = AddElectroDaylyForm
    template_name = 'meters/add_electro.html'
    title_page = 'Добавление суточного показания'
    success_url = reverse_lazy('meters:electro')  # URL по умолчанию

    def form_valid(self, form):
        c = self.get_mixin_context()
        tarif_id = c['tarif_id']
        address_id = c['address_id']
        # Получаем объект без сохранения его в базу данных
        instance  = form.save(commit=False)
        f = form.cleaned_data
        dr = f['date_reading']  # дата занесения для слага
        address_slug = self.kwargs['address_slug']
        instance.slug = f'{address_slug}-{dr.strftime("%Y-%m")}'
        instance.tar = Tarif.objects.get(id=tarif_id)
        instance.addr_id = address_id

        instance.author = self.request.user

        instance.save()

        url = reverse( 'meters:electro', kwargs={'addr_slug': address_slug})
        return redirect( url )
        #return super().form_valid(form)


    def get_context_data(self, **kwargs):
        # c = self.get_mixin_context()
        # address_name = c['address_name']
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class NewElectro(DataMixin, CreateView):
    model = Electro
    form_class = NewElectroForm
    template_name = 'meters/add_electro.html'
    title_page = 'Создать показание'
    success_url = reverse_lazy('meters:home')  # URL по умолчанию

    def form_valid(self, form):
        c = self.get_mixin_context()
        #tarif_id = c['tarif_id']
        address_id = c['address_id']
        # Получаем объект без сохранения его в базу данных
        instance = form.save(commit=False)
        f = form.cleaned_data
        dr = f['date_reading']  # дата занесения для слага
        address_slug = self.kwargs['address_slug']
        instance.slug = f'{address_slug}-{dr.strftime("%Y-%m")}'
        #instance.tar = Tarif.objects.get(id=tarif_id)
        instance.addr_id = address_id

        instance.author = self.request.user

        instance.save()

        url = reverse('meters:electro', kwargs={'addr_slug': address_slug})
        return redirect(url)
        #return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = self.get_mixin_context(context)
        return self.get_mixin_context(context)


#----------------------------------------------------------------------------------------------
class AddWater( DataMixin, CreateView  ):
    model = Water
    form_class = AddWaterForm
    template_name = 'meters/add_water.html'
    title_page = 'Добавление показания'
    success_url = reverse_lazy('meters:home')  # URL по умолчанию

    def form_valid(self, form):
        c = self.get_mixin_context()
        address_id = c['address_id']
        # Получаем объект без сохранения его в базу данных
        instance  = form.save(commit=False)
        f = form.cleaned_data
        dr = f['date_reading']  # дата занесения для слага
        address_slug = self.kwargs['address_slug']
        instance.slug = f'{address_slug}-{dr.strftime("%Y-%m")}'
        instance.addr_id = address_id

        instance.author = self.request.user

        instance.save()

        url = reverse('meters:water', kwargs={'addr_slug': address_slug})
        return redirect(url)
        #return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class NewWater(DataMixin, CreateView):
    model = Water
    form_class = NewWaterForm
    template_name = 'meters/add_water.html'
    title_page = 'Создать показание'
    success_url = reverse_lazy('meters:home')  # URL по умолчанию

    def form_valid(self, form):
        c = self.get_mixin_context()
        address_id = c['address_id']
        # Получаем объект без сохранения его в базу данных
        instance = form.save(commit=False)
        f = form.cleaned_data
        dr = f['date_reading']  # дата занесения для слага
        address_slug = self.kwargs['address_slug']
        instance.slug = f'{address_slug}-{dr.strftime("%Y-%m")}'
        instance.addr_id = address_id

        instance.author = self.request.user

        instance.save()

        url = reverse('meters:water', kwargs={'addr_slug': address_slug})
        return redirect(url)
        #return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'meters/contact.html'
    success_url = reverse_lazy('meters:home')
    title_page = "Обратная связь"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
@login_required     #(login_url='/admin/')
def about(request):
    return render(request, 'meters/about.html', {'title': 'О сайте'})
# ---------------------------------------------------------------------------------------------

def login(request):
    return HttpResponse("Авторизация")

# ---------------------------------------------------------------------------------------------
# Срабатывает, если в любом представлении возн ош 404  , руками:    raise Http404()
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
