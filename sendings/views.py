from django.urls import reverse
from django.http import HttpResponseRedirect
from archives.models import Archives
import telebot


def tel(request, id):
    myarchives = Archives.objects.get(id=id)
    token = "5655170166:AAG2MrYcLmqeBPyCI-Bvo38Mlj3qjbg4FSQ"
    chat_id = "5740110040"
    bot = telebot.TeleBot(token)
    msg = f"{myarchives.dat}:\nUSD {myarchives.usd}\nEUR {myarchives.eur}\nRUB {myarchives.rub}"
    bot.send_message(chat_id, msg)
    return HttpResponseRedirect(reverse("index"))


def vib(request, id):
    pass

