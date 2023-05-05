from . import views
from django.urls import path

urlpatterns = [
    path("", views.adminhome),
    path("manageoptions/",views.manageoptions),
    path("manageusers/",views.manageusers),
    path("manageuserstatus/",views.manageuserstatus),
    path("addcategory/",views.addcategory),
    path("addsubcategory/",views.addsubcategory),
    path("addproperty/",views.addproperty),
    path("fetchSubCatAJAX/",views.fetchSubCatAJAX)
]






