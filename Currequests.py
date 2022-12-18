import requests
#dat = input("Введите дату")
dat = "2020-10-10"
usdapi = requests.get(f"https://www.nbrb.by/api/exrates/rates/USD?parammode=2&ondate={dat}")
usdres=dict(usdapi.text)
#usdcur=usdres[usdres.rfind(":")+1:len(usdres)-1]
# usd = {
#     "Cur_ID":431,
#     "Date":"2022-10-10T00:00:00",
#     "Cur_Abbreviation":"USD",
#     "Cur_Scale":1,
#     "Cur_Name":"Доллар США",
#     "Cur_OfficialRate":2.5367
#     }
#print(f"курс usd на дату {dat} составляет {usdcur}")
print(usdres)
