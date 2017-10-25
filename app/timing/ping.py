from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def init_timing(app):

    def tick():
        print('Tick! The time is: %s' % datetime.now())
        # verbose_ping("google.com")
        # verbose_ping("baidu.com")

    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(tick, 'interval', seconds=10)
    scheduler.start()
