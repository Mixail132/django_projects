from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Archives, ValueErrorException, DateDoesNotExistYet
from django.contrib.auth.models import User
import requests

from datetime import timedelta, date, datetime
import time
#from ..sendings.views import tel


def index(request):
    """Отобразить данные"""
    archives = Archives.objects.all().values()
    Addings.addtodayrecord()
    myarchives = sorted(archives, key=lambda e: e["dat"])
    template = loader.get_template("archives.html")
    context = {"myarchives": myarchives,}
    return HttpResponse(template.render(context, request))

def updatebyapi(dat):
    myarchives = Archives.objects.get(dat=dat)
    currencies = ["USD", "EUR", "RUB" ]
    for cur in currencies:
        exec(f'api = requests.get(f"https://www.nbrb.by/api/exrates/rates/{cur}?parammode=2&ondate={dat}").text')
        exec(f'myarchives.{cur.lower()} = api[api.rfind(":") + 1:len(api) - 1]')
        myarchives.save()

def updaterecord(request):
    """Обновить данные за указанный период"""
    m = Archives.objects.values()
    today = datetime.today().date()
    if fdate > today :
         raise DateDoesNotExistYet("The date you input has not yet come :)")
    for dates in daterange(sdate, fdate):
        for i in range(len(m)):
            if dates == m[i]["dat"]:
                updatebyapi(dates)
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

#archives = Archives.objects.values()
class Addings:
    def addrecord(request):
        """ Добавить строки в таблицу без данных за указанный период"""
        archives = Archives.objects.values()
        for dates in daterange(sdate, fdate):
            for i in range(len(archives)):
                if dates == archives[i]["dat"]:
                    break
            else:
                t = dates.strftime("%Y-%m-%d")
                data = Archives(dat=t)
                data.save()
        return HttpResponseRedirect(reverse("index"))

    def addtodayrecord():
        archives = Archives.objects.values()
        dates = datetime.today().date()
        data = Archives(dat=dates)
        for i in range(len(archives)):
              if dates == archives[i]["dat"]:
                break
        else:
            data.save()
        if data.usd == 0 and data.eur == 0 and data.rub == 0:
            try:
                updatebyapi(dates)
            except:
                pass  # здесь можно вывести сообщение alert о том, что связи нет

def showperiod(request):
    pass

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



