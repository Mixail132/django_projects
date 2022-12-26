from django.urls import path
from . import views

urlpatterns = [
    path("tel/<int:id>", views.tel, name="tel"),
    ]