from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Archives
import requests


def index(request):
    myarchives = Archives.objects.all().values()
    template = loader.get_template("archives.html")
    context = {"myarchives": myarchives,}
    return HttpResponse(template.render(context, request))


def add(request):
    template = loader.get_template("add.html")
    return HttpResponse(template.render({}, request))


def update(request,id):
    myarchives = Archives.objects.get(id=id)
    dat = myarchives.dat
    usdapi = requests.get(f"https://www.nbrb.by/api/exrates/rates/USD?parammode=2&ondate={dat}")
    eurapi = requests.get(f"https://www.nbrb.by/api/exrates/rates/EUR?parammode=2&ondate={dat}")
    rubapi = requests.get(f"https://www.nbrb.by/api/exrates/rates/RUB?parammode=2&ondate={dat}")
    usdres = usdapi.text
    eurres = eurapi.text
    rubres = rubapi.text
    usdcur = usdres[usdres.rfind(":") + 1:len(usdres) - 1]
    eurcur = eurres[eurres.rfind(":") + 1:len(eurres) - 1]
    rubcur = rubres[rubres.rfind(":") + 1:len(rubres) - 1]
    myarchives.usd = usdcur
    myarchives.eur = eurcur
    myarchives.rub = rubcur
    myarchives.save()
    return HttpResponseRedirect(reverse("index"))

# def update(request,id):
#     """ The update view does the following:
#     Gets the id as an argument.
#     Uses the id to locate the correct record in the Archiver table.
#     loads a template called update.html.
#     Creates an object containing the member.
#     Sends the object to the template.
#     Outputs the HTML that is rendered by the template."""
#     myarchives = Archives.objects.get(id=id)
#     template = loader.get_template("update.html")
#     context = {"myarchives": myarchives,}
#     return HttpResponse(template.render(context, request))

def delete(request,id):
    myarchives = Archives.objects.get(id=id)
    myarchives.usd = 0
    myarchives.eur = 0
    myarchives.rub = 0
    #myarchives.delete()
    myarchives.save()
    return HttpResponseRedirect(reverse("index"))


def addrecord(request):
    d = request.POST["dat"]
    u = request.POST["usd"]
    e = request.POST["eur"]
    dat = Archives(dat=d, usd=u, eur=e)
    dat.save()
    return HttpResponseRedirect(reverse("index"))


def updaterecord(request, id):
    d = request.POST["dat"]
    u = request.POST["usd"]
    e = request.POST["eur"]
    data = Archives.objects.get(id=id)
    data.dat = d
    data.usd = u
    data.eur = e
    data.save()
    return HttpResponseRedirect(reverse("index"))

