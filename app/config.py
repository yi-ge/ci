DB_USER = 'test'
DB_PASSWORD = 'test'
DB_HOST = 'localhost'
DB_DB = 'ci'

DEBUG = True
PORT = 5001
HOST = "0"
SECRET_KEY = "test"

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DB
