#coding=utf-8
import paramiko
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
CORS(app)

jwt = JWT(app, authenticate, identity)

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    realname = Column(String(10))
    password = Column(String(255))

DBSession = sessionmaker(bind=engine)

timestamp = time.mktime(datetime.datetime.now().timetuple())

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

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return jsonify({ 'status': 1 })

@app.route('/login', methods=['POST'])
def login():
    if valid_login(request.form['username'],
        request.form['password']):
        payload = { 'username': request.form['username'] }
        return jsonify({ 'status': 1 , 'result': { 'token': jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=5))}})
    else:
        return jsonify({ 'status': 403 })

def sendsms():
    response = requests.get('https://httpbin.org/ip')
    print('Your IP is {0}'.format(response.json()['origin']))
