from django.urls import path
from . import views

# П А К Е Т    П Р И Л О Ж Е Н И Я  meters

app_name = "meters"

urlpatterns = [
    path( '', views.MetersHome.as_view(),   name='home' ),

    path('address/<int:addr_id>/', views.address, name='address'),

    path('electro/<slug:addr_slug>/', views.ShowElectro.as_view(), name='electro'),
    path('water/<slug:addr_slug>/', views.ShowWater.as_view(), name='water'),

    path('itemelectro/<slug:eitem_slug>/', views.ItemElectro.as_view(), name='item_electro'),
    path('itemwater/<slug:witem_slug>/', views.ItemWater.as_view(), name='item_water'),

    path('addelectro/<slug:address_slug>/', views.AddElectro.as_view(), name='add_electro'),
    path('addelectroDayly/<slug:address_slug>/', views.AddElectroDayly.as_view(), name='add_electro_dayly'),
    path('newelectro/<slug:address_slug>/', views.NewElectro.as_view(), name='new_electro'),

    path('addwater/<slug:address_slug>/', views.AddWater.as_view(), name='add_water'),
    path('newwater/<slug:address_slug>/', views.NewWater.as_view(), name='new_water'),

    path('selector/<slug:type_meters>/<slug:addr_slug>/', views.SelectorService.as_view(), name='selector'),

    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),

    path('contact/', views.ContactFormView.as_view(), name='contact'),
]