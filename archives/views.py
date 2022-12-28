from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Archives, ValueErrorException, DateDoesNotExistYet
from django.contrib.auth.models import User
import requests
from datetime import timedelta, date, datetime

def index(request):
    """Отобразитьd данные"""
    archives = Archives.objects.all().values()
    myarchives = sorted(archives, key=lambda e: e["dat"])
    template = loader.get_template("archives.html")
    context = {"myarchives": myarchives,}
    return HttpResponse(template.render(context, request))

def updaterecord(request):
    """Обновить данные за указанный период"""
    m = Archives.objects.values()
    today = datetime.today().date()
    if fdate > today:
         raise DateDoesNotExistYet("The date you input has not yet come :)")
    for dates in daterange(sdate, fdate):
        for i in range(len(m)):
            if dates == m[i]["dat"]:
                myarchives = Archives.objects.get(dat=dates)
                dat = myarchives.dat
                usdapi = requests.get(f"https://www.nbrb.by/api/exrates/rates/USD?parammode=2&ondate={dat}")
                eurapi = requests.get(f"https://www.nbrb.by/api/exrates/rates/EUR?parammode=2&ondate={dat}")
                rubapi = requests.get(f"https://www.nbrb.by/api/exrates/rates/RUB?parammode=2&ondate={dat}")
                usdres = usdapi.text
                eurres = eurapi.text
                rubres = rubapi.text
                myarchives.usd = usdres[usdres.rfind(":") + 1:len(usdres) - 1]
                myarchives.eur = eurres[eurres.rfind(":") + 1:len(eurres) - 1]
                myarchives.rub = rubres[rubres.rfind(":") + 1:len(rubres) - 1]
                myarchives.save()
    return HttpResponseRedirect(reverse("index"))

def daterange(startdate, finaldate):
    """Определить диапазон по заданным датам"""
    for n in range(int((finaldate - startdate).days) + 1):
        yield startdate + timedelta(n)

def delrecord(request):
    """Удалить строки из таблицы за указанный период"""
    for dates in daterange(sdate, fdate):
        m = Archives.objects.values()
        for i in range(len(m)):
            if dates == m[i]["dat"]:
                data = Archives.objects.all()[i]
                data.delete()
    return HttpResponseRedirect(reverse("index"))

def addrecord(request):
    """ Добавить строки в таблицу без данных за указанный период"""
    m = Archives.objects.values()
    for dates in daterange(sdate, fdate):
        for i in range(len(m)):
            if dates == m[i]["dat"]:
                break
        else:
            t = dates.strftime("%Y-%m-%d")
            data = Archives(dat=t)
            data.save()
    return HttpResponseRedirect(reverse("index"))

def do(request):
    """Определить выбранное действие за указанный период"""
    user=request.user
    if user.is_authenticated:
        sdat = request.POST["sdat"].split("-")
        fdat = request.POST["fdat"].split("-")
        global sdate
        global fdate
        try:
            sdate = date(int(sdat[0]),int(sdat[1]),int(sdat[2]))
            fdate = date(int(fdat[0]),int(fdat[1]),int(fdat[2]))
        except (ValueError):
            msg = "You did not input correct dates"
            return render(request, "valerror.html", {"msg": msg})
        if sdate > fdate:
            msg = "Your period ends earlier than it starts:)"
            raise ValueErrorException (msg)
        adds = request.POST["doing"]
    else:
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse (f"{adds}"))


print(datetime.today().date())
