DB_USER = 'ci'
DB_PASSWORD = 'soBEkGz0nwssshpT'
DB_HOST = 'localhost'
DB_DB = 'ci'

DEBUG = True
PORT = 5000
HOST = "0"
SECRET_KEY = "test"

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DB
