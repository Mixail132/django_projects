from django.urls import path
from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("tel/<int:id>", views.tel, name="tel"),
    path("vib/<int:id>", views.vib, name="vib"),
]