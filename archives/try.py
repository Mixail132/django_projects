import schedule
import time

def job():
    print("123")

schedule.every().second.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)