from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("del/", views.delete, name="del"),
    path("del/delrecord/",  views.delrecord, name="delrecord"),
    path("add/addrecord/",  views.addrecord, name="addrecord"),
    path("update/<int:id>", views.update,    name="update"),
    #path("update/updaterecord/<int:id>", views.updaterecord, name="updaterecord"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("deleteselected/", views.deleteselected, name="deleteselected"),
    path("deletestring/<int:id>", views.deletestring, name="deletestring"),
]