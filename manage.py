#coding=utf-8
# import MySQLdb
import paramiko
import time
import requests
import sqlite3
import python_jwt as jwt, Crypto.PublicKey.RSA as RSA, datetime

key = RSA.generate(2048)
payload = { 'foo': 'bar', 'wup': 90 };
token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=5))
header, claims = jwt.verify_jwt(token, key, ['PS256'])
for k in payload: assert claims[k] == payload[k]
print(header)

response = requests.get('https://httpbin.org/ip')

print('Your IP is {0}'.format(response.json()['origin']))

#timestamp
timestamp = time.mktime(datetime.datetime.now().timetuple())

#创建SSH对象
ssh = paramiko.SSHClient()

#把要连接的机器添加到known_hosts文件中
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#连接服务器
ssh.connect(hostname='', port=22, username='root', password='')

memCmd = 'ls'
#cmd = 'ls -l;ifconfig'       #多个命令用;隔开
stdin, stdout, stderr = ssh.exec_command(memCmd)

memResult = stdout.read()

if not memResult:
    memResult = stderr.read()
ssh.close()

print(memResult.decode())
#
# conn= MySQLdb.connect(
#         host='localhost',
#         port = 3306,
#         user='root',
#         passwd='test123',
#         db ='test54',
#         )
# cur = conn.cursor()
#
# #创建数据表
# #创建数据表
# #cur.execute("create table meminfo(id int ,timestamp varchar(30),used varchar(20))")
#
# #插入一条数据
# #cur.execute("insert into meminfo values('1','%s','%s')" % (memResult,timestamp))
#
# #修改查询条件的数据
# #cur.execute("update meminfo set used='0' where id = 0")
#
# #删除查询条件的数据
# #cur.execute("delete from meminfo")
#
# cur.close()
# conn.commit()
# conn.close()
