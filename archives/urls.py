from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("do/", views.do, name="do"),
    path("delrecord/", views.delrecord, name="delrecord"),
    path("addrecord/", views.addrecord, name="addrecord"),
    path("updaterecrd", views.updaterecord, name="updaterecord"),

    ]
