#from django.test import TestCase
import requests
import time
from datetime import datetime, timedelta
def connection ():
    """Протестировать длительность соединения с конкретным API"""
    now_time = time.time()
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    requests.get(f"https://www.nbrb.by/api/exrates/rates/USD?parammode=2&ondate={yesterday}")
    requests.get(f"https://www.nbrb.by/api/exrates/rates/EUR?parammode=2&ondate={yesterday}")
    requests.get(f"https://www.nbrb.by/api/exrates/rates/RUB?parammode=2&ondate={yesterday}")
    dif_time = time.time() - now_time
    return dif_time

assert connection() < 20, "Connection time is too long, the remote server does not answer!"


