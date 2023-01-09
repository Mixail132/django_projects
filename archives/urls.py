from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("do/", views.do, name="do"),
    path("delrecord/", views.delrecord, name="delrecord"),
    path("addrecord/", views.Addings.addrecord, name="addrecord"),
    path("updaterecord/", views.updaterecord, name="updaterecord"),
    path("showperiod/", views.showperiod, name = "showperiod"),
    ]
