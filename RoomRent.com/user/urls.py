from django.urls import path

from . import views

urlpatterns = [
    path("", views.userhome),
    path("searchproperty/", views.searchproperty),
    path("searchsubcategory/", views.searchsubcategory),
    path("viewproperty/", views.viewproperty),
    path("epuser/",views.epuser),
    path("cpuser/",views.cpuser)
]




