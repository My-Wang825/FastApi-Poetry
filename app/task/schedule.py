from task.cron.nifi_dingding_alarm import nifi_alarm_to_dingding
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()

# 定时任务
# scheduler.add_job(nifi_alarm_to_dingding, 'interval', minutes=10)
