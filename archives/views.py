from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Archives
import requests
from datetime import timedelta, date
def index(request):
    s = "2022-12-12"
    e = "2022-12-12"
    archives = Archives.objects.all().values()
    myarchives = sorted(archives, key = lambda e :e["dat"])
    template = loader.get_template("archives.html")
    context = {"myarchives": myarchives,}
    return HttpResponse(template.render(context, request))

def add(request):
    template = loader.get_template("add.html")
    return HttpResponse(template.render({}, request))

def delete(request):
    template = loader.get_template("delete.html")
    return HttpResponse(template.render({}, request))

def updaterecord(request):
    m = Archives.objects.values() # m - список словарей
    for dates in daterange(sdate, fdate):
        for i in range(len(m)):
            if dates == m[i]["dat"]: # i  элемент списка по порядку, m - ключ "dat" вложенного словаря
                myarchives = Archives.objects.get(dat=dates)
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

def daterange(startdate, finaldate):
    for n in range(int((finaldate - startdate).days) + 1):
        yield startdate + timedelta(n)

def delrecord(request):
    for dates in daterange(sdate, fdate):
        m = Archives.objects.values()
        for i in range(len(m)):
            if dates == m[i]["dat"]: # i  элемент списка по порядку, m - ключ "dat" вложенного словаря
                data = Archives.objects.all()[i]
                data.delete()
    return HttpResponseRedirect(reverse("index"))

def addrecord(request):
    m = Archives.objects.values() # m - список словарей
    for dates in daterange(sdate, fdate):
        for i in range(len(m)):
            if dates == m[i]["dat"]: # i  элемент списка по порядку, m - ключ "dat" вложенного словаря
                break
        else: # работает только после break
            t = dates.strftime("%Y-%m-%d") #  делаем из даты строку
            data = Archives(dat=t)
            data.save()
    return HttpResponseRedirect(reverse("index"))

def do(request):
    sdat = request.POST["sdat"].split("-")
    fdat = request.POST["fdat"].split("-")
    global sdate
    global fdate
    sdate = date(int(sdat[0]),int(sdat[1]),int(sdat[2]))
    fdate = date(int(fdat[0]),int(fdat[1]),int(fdat[2]))
    adds = request.POST["doing"]
    return HttpResponseRedirect(reverse (f"{adds}"))

