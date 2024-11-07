from django.urls import path
from . import views

# П А К Е Т    П Р И Л О Ж Е Н И Я

urlpatterns = [
    path( '', views.index,   name='index' ),

]





