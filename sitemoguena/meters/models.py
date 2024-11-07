from django.db import models

from django.contrib.auth import get_user_model
from django.urls import reverse

class Address( models.Model ):
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name="slug")  # tchelabinsk-martchenko
    city = models.CharField(max_length=50, verbose_name="Город")
    street = models.CharField(max_length=50, verbose_name="Улица")

    def __str__(self):
        return f'{self.city}, {self.street}'

    class Meta:
        #db_table = 'meters_address'
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def get_absolute_url(self):
        return reverse('meters:address', kwargs={'slug': self.slug})



class ElectroManager( models.Manager  ):
    def by_address(self, addr_id):
        # Метод для фильтрации по полю addr_id
        return self.filter( addr_id=addr_id )

class WaterManager( models.Manager  ):
    def by_address(self, addr_id):
        # Метод для фильтрации по полю addr_id
        return self.filter( addr_id=addr_id )




class Electro( models.Model ):
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="Slug")
    # %Y-%m-tchelabinsk-martchenko
    nighttime = models.IntegerField(  blank=True, default=0, verbose_name="Ночь" )
    daytime =   models.IntegerField(  blank=True, default=0, verbose_name="День" )
    dayly =     models.IntegerField(  blank=True, default=0, verbose_name="Сутки" )
    date_reading = models.DateField( verbose_name="Снятие" )
    date_create = models.DateTimeField( auto_now_add=True, verbose_name="Занесение")
    date_update = models.DateTimeField( auto_now=True, verbose_name="Изменение")
    # addr = models.ForeignKey('Address', on_delete=models.PROTECT, related_name='el', verbose_name="Адрес" )
    # tar = models.ForeignKey('Tarif', on_delete=models.PROTECT,    related_name='tr', verbose_name="Тариф" )
    addr = models.ForeignKey('Address', on_delete=models.PROTECT, related_name='address', verbose_name="Адрес" )
    tar = models.ForeignKey('Tarif', on_delete=models.PROTECT,    related_name='tarif', verbose_name="Тариф" )
    author = models.ForeignKey( get_user_model(), on_delete=models.SET_NULL, null=True,
                                related_name='electros', default=None )
    models.OneToOneField
    objects = models.Manager()
    emanager = ElectroManager()

    def __str__(self):
        #d = self.date_reading.strftime("%Y-%m")
        d = self.date_reading
        return f'{d}: {self.daytime}, {self.nighttime}, {self.dayly}'

    class Meta:
        verbose_name = 'Электроснабжение'
        verbose_name_plural = 'Электроснабжение'
        ordering = ['-date_reading']    # сортировка по умолчанию для выборки
        indexes = [                     # создание индексов
            models.Index(fields=['-date_reading'])
        ]

    def get_absolute_url(self):
        return reverse('meters:item_electro', kwargs={'eitem_slug': self.slug})

    def previous_indication(self):
        # Получаем предыдущую запись по дате, если она есть
        #previous_record = Electro.objects.all().earliest( 'date_reading')
        #previous_record = Electro.objects.filter(date_reading__lt=self.date_reading).order_by('-date_reading').first()

        ###previous_record = Electro.objects.filter(  date_reading__lt=self.date_reading  ).first()
        previous_record = Electro.emanager.by_address(self.addr_id).filter(date_reading__lt=self.date_reading).first()

        if previous_record:
            return  {'dayly': previous_record.dayly,
                     'nighttime': previous_record.nighttime,
                     'daytime': previous_record.daytime
                     }
        return None

    @property
    def difference(self):
        # Вычисляем разность с предыдущей записью
        prev_indication = self.previous_indication()
        if prev_indication is not None:
            return {'dayly':self.dayly - prev_indication['dayly'],
                    'nighttime':self.nighttime - prev_indication['nighttime'],
                    'daytime':self.daytime - prev_indication['daytime']
                   }
        return None

class Water( models.Model ):
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="Slug")
    hot = models.IntegerField(blank=True, default=0, verbose_name="Горячая")
    cold = models.IntegerField(blank=True, default=0, verbose_name="Холодная")
    date_reading = models.DateField( verbose_name="Снятие")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Занесение")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Изменение")
    addr = models.ForeignKey('Address', on_delete=models.PROTECT, related_name='addresses', verbose_name="Адрес" )
    author = models.ForeignKey( get_user_model(), on_delete=models.SET_NULL, null=True,
                               related_name='waters', default=None)

    objects = models.Manager()
    wmanager = WaterManager()

    def __str__(self):
        d = self.date_reading #.strftime("%Y-%m")
        return f'{d}: {self.hot}, {self.cold}'

    class Meta:
        verbose_name = 'Водоснабжение'
        verbose_name_plural = 'Водоснабжение'
        ordering = ['-date_reading']
        indexes = [
            models.Index(fields=['-date_reading'])
        ]

    def get_absolute_url(self):
        return reverse('meters:item_water', kwargs={'witem_slug': self.slug})

    def previous_indication(self):
        # Получаем предыдущую запись по дате, если она есть
        #previous_record = Water.objects.filter(date_reading__lt=self.date_reading).first()
        previous_record = Water.wmanager.by_address(self.addr_id).filter(date_reading__lt=self.date_reading).first()
        if previous_record:
            return  {'hot': previous_record.hot,
                     'cold': previous_record.cold,
                     }
        return None

    @property
    def difference(self):
        # Вычисляем разность с предыдущей записью
        prev_indication = self.previous_indication()
        if prev_indication is not None:
            return {'hot':self.hot - prev_indication['hot'],
                    'cold':self.cold - prev_indication['cold'],
                    }
        return None


class Tarif(models.Model):
    slug = models.SlugField(max_length=10, unique=True, db_index=True, verbose_name="Slug") # tarif-0/1/2
    name = models.CharField( max_length=25, verbose_name="Имя тарифа" )
    number = models.IntegerField(  verbose_name="Номер тарифа")

    def __str__(self):
        return f'{self.number}-{self.name}'

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
