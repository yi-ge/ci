from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
# scheduler.add_executor('processpool')


def init_timing(app):

    @scheduler.scheduled_job('interval', seconds=5)
    def tick():
        print('Tick! The time is: %s' % datetime.now())
        # verbose_ping("google.com")
        # verbose_ping("baidu.com")

    scheduler.start()
