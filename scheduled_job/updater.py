from apscheduler.schedulers.background import BackgroundScheduler
from scheduled_job.lesson_controller import *

class jobs:
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')
    # scheduler.add_job(job_create_lesson, 'cron', hour=0, minute=0, second=1)
    # scheduler.add_job(job_start_lesson, 'interval', minutes=1)