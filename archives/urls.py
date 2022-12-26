from django.urls import path
from . import views

urlpatterns = [
    path("",                      views.index,           name="index"),
    path("add/",                  views.add,             name="add"),
    path("del/",                  views.delete,          name="del"),
    path("do/",                   views.do,              name="do"),
    path("del/delrecord/",        views.delrecord,       name="delrecord"),
    path("add/addrecord/",        views.addrecord,       name="addrecord"),
    # path("update/<int:id>",       views.update,          name="update"),
    path("updaterecrd",           views.updaterecord,    name="updaterecord"),
    #path("update/updaterecord/<int:id>", views.updaterecord, name="updaterecord"),
    # path("delete/<int:id>",       views.delete,          name="delete"),
    # path("deletestring/<int:id>", views.deletestring,    name="deletestring"),
]