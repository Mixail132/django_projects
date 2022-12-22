from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Archives
import requests
from datetime import timedelta, date
def index(request):
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

def delrecord(request):
    sdat = request.POST["sdat"].split("-")
    fdat = request.POST["fdat"].split("-")
    sdate = date(int(sdat[0]), int(sdat[1]), int(sdat[2]))
    fdate = date(int(fdat[0]), int(fdat[1]), int(fdat[2]))
    def daterange(startdate, finaldate):
        for n in range(int((finaldate - startdate).days) + 1):
            yield startdate + timedelta(n)
    for dates in daterange(sdate, fdate):
        m = Archives.objects.values()
        for i in range(len(m)):
            if dates == m[i]["dat"]: # i  элемент списка по порядку, m - ключ "dat" вложенного словаря
                data = Archives.objects.all()[i]
                data.delete()
    return HttpResponseRedirect(reverse("index"))

def deletestring(request,id):
    myarchives = Archives.objects.get(id=id)
    myarchives.delete()
    return HttpResponseRedirect(reverse ("index"))

def addrecord(request):
    sdat = request.POST["sdat"].split("-")
    fdat = request.POST["fdat"].split("-")
    # получили из полей <input > формы HTML с именами fdat и sdat
    # значения ввиде строки через дефис ГГГГ-ММ-ДД и сделали его списком
    sdate = date(int(sdat[0]),int(sdat[1]),int(sdat[2]))
    fdate = date(int(fdat[0]),int(fdat[1]),int(fdat[2]))
    # превратили каждый элемент списка в число и передали в функцию
    # date (как она того требует) библиотеки datetime
    def daterange(startdate, finaldate):
        for n in range(int((finaldate-startdate).days)+1):
            yield startdate + timedelta(n)

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

def deleteselected (request, id):
    myarchives = Archives.objects.get(id=id)
    myarchives.delete()
    #Archives(dat=i, usd = 0, eur = 0, rub = 0)
        #data.save()

    # myarchives = Archives.objects.get(id=id)
    # myarchives.usd = 0
    # myarchives.eur = 0
    # myarchives.rub = 0
    #myarchives.delete()
    # myarchives.save()
    return HttpResponseRedirect(reverse("index"))
