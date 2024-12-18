import requests
import schedule
import time
import datetime
# ...existing code...

def job():
    print("I'm working...", datetime.datetime.now())


def main():
    schedule.every(5).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
