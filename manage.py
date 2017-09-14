#coding=utf-8
import paramiko
import requests
import jwt, datetime, time
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.debug = True
CORS(app)

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
SECRET_KEY = 'd21kljk21ljk2e'

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    realname = Column(String(10))
    password = Column(String(255))

DBSession = sessionmaker(bind=engine)

# timestamp = time.mktime(datetime.datetime.now().timetuple())

# #创建SSH对象
# ssh = paramiko.SSHClient()
#
# #把要连接的机器添加到known_hosts文件中
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# #连接服务器
# ssh.connect(hostname='', port=22, username='root', password='')
#
# memCmd = 'ls'
# #cmd = 'ls -l;ifconfig'       #多个命令用;隔开
# stdin, stdout, stderr = ssh.exec_command(memCmd)
#
# memResult = stdout.read()
#
# if not memResult:
#     memResult = stderr.read()
# ssh.close()

# print(memResult.decode())

# @staticmethod
def encode_auth_token(user_id, username, login_time):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
            'iat': datetime.datetime.utcnow(),
            'iss': 'ken',
            'data': {
                'id': user_id,
                'username': username,
                'login_time': login_time
            }
        }
        print(payload)
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return str(e)

def valid_login(username, password):
    return True

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return jsonify({ 'status': 1 })

@app.route('/login', methods=['POST'])
def login():
    if valid_login(request.form['username'],
        request.form['password']):
        token = encode_auth_token('test', request.form['username'], datetime.datetime.utcnow())
        print(token)
        print('开始解码')
        # print(jwt.decode(token, 'SECRET_KEY', leeway=10, algorithms=['HS256']))
        # return jsonify({ 'status': 1, 'result': { 'token': token}})
        return 'xxx'
    else:
        return jsonify({ 'status': 403 })

def sendsms():
    response = requests.get('https://httpbin.org/ip')
    print('Your IP is {0}'.format(response.json()['origin']))

@app.errorhandler(404)
def bad_request(e):
    return jsonify({ 'status': 404 }), 404

@app.errorhandler(500)
def bad_request(e):
    return jsonify({ 'status': 500 }), 500
