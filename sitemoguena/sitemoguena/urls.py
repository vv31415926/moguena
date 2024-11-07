"""
URL configuration for sitemoguena project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found

from sitemoguena import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path( '',           include( 'mainapp.urls'                      ) ),
    path( 'meters/',    include( 'meters.urls', namespace='meters'  ) ),
    path( 'users/',     include( 'users.urls',  namespace='users' ) ),

    path('social-auth/', include('social_django.urls', namespace='social')),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# обработчик для случая отсутствия страницы: что делать при 404
# срабатывает при отключении отладки DEBUG=False
handler404 = page_not_found

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Жилищно коммунальное хозяйство"


