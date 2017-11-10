from datetime import datetime
from flask_apscheduler import APScheduler


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'job1',
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 10
        }
    ]

    SCHEDULER_API_ENABLED = True


def job1(a, b):
    print(str(a) + ' ' + str(b))


def init_timing(app):
    app.config.from_object(Config())

    scheduler = APScheduler()
    # it is also possible to enable the API directly
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()
