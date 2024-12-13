import requests
import schedule
import time
# ...existing code...

def job():
    response = requests.get('http://localhost:8008/')
    print(response.json())

def main():
    schedule.every(5).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
