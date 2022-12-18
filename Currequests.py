import requests

# dat = "2020-10-10"
# usdapi = requests.get(f"https://www.nbrb.by/api/exrates/rates/USD?parammode=2&ondate={dat}")
# eurapi = requests.get(f"https://www.nbrb.by/api/exrates/rates/EUR?parammode=2&ondate={dat}")
# usdres = usdapi.text
# eurres = eurapi.text
# usdcur = usdres[usdres.rfind(":")+1:len(usdres)-1]
# eurcur = eurres[eurres.rfind(":")+1:len(eurres)-1]
# print(f"курс USD на дату {dat} составляет {usdcur}")
# print(f"курс EUR на дату {dat} составляет {eurcur}")

# def send_msg(text):
#     token = "5655170166:AAG2MrYcLmqeBPyCI-Bvo38Mlj3qjbg4FSQ"
#     chat_id = "5740110040"
#     url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
#     results = requests.get(url_req)
#     #print(results.json())
 
# send_msg("Hello Misha!")

 
import telebot
 
token = '5655170166:AAG2MrYcLmqeBPyCI-Bvo38Mlj3qjbg4FSQ'
bot = telebot.TeleBot(token)
chat_id = '5740110040'
text = 'Hello python'
bot.send_message(chat_id, text)
