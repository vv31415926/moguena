from django.urls import path
from . import views

# П А К Е Т    П Р И Л О Ж Е Н И Я  VideoImg

app_name = "videoimg"

urlpatterns = [
    path( '', views.Home.as_view(),   name='home' ),

]












