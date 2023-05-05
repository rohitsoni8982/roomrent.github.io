from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings

from django.views.static import serve
from django.conf.urls import url

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.home),
    path("about/",views.about),
    path("contact/",views.contact),
    path("service/",views.service),
    path("register/",views.register),
    path("verify/",views.verify),
    path("checkEmailAvaibility/",views.checkEmailAvaibility),
    path("login/",views.login),
    path("myadmin/",include('myadmin.urls')),
    path("user/",include('user.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




