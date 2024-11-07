from django.contrib import admin

from .models import Electro, Water, Address, Tarif


@admin.register( Address )
class AddressAdmin( admin.ModelAdmin ):
    list_display = ( 'id', 'street', 'city', 'slug' )
    list_display_links = ('id', 'street')
    list_per_page = 10
    ordering = ['city', 'street']

@admin.register( Electro )
class ElectroAdmin( admin.ModelAdmin ):
    list_display = ( 'id', 'date_reading', 'daytime', 'nighttime', 'dayly', 'addr', 'tar', 'slug' )
    list_display_links = ( 'id', 'date_reading' )
    #list_editable = ( 'addr', )
    list_per_page = 10
    ordering = [ '-date_reading']

@admin.register( Water )
class WaterAdmin( admin.ModelAdmin ):
    list_display = ( 'id', 'date_reading', 'hot', 'cold', 'addr', 'slug' )
    list_display_links = ('id', 'date_reading')
    list_per_page = 10
    ordering = ['-date_reading']



@admin.register( Tarif )
class TarifAdmin( admin.ModelAdmin ):
    list_display = ( 'id', 'name', 'number', 'slug' )
    list_display_links = ('id', 'name')
    list_per_page = 10
    ordering = ['name']

