from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Ping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, unique=False, nullable=True)
    result = db.Column(db.Integer, unique=False, nullable=True)
    time = db.Column(db.DateTime, unique=False, nullable=True)

    def __init__(self, name, ip, auth, sshkey, password, address, note, status, type):
        self.name = name
        self.ip = ip
        self.auth = auth
        self.sshkey = sshkey
        self.password = password
        self.address = address
        self.note = note
        self.status = status
        self.type = type

    def __str__(self):
        return "Server(id='%s')" % self.id

    def get(self, id):
        return self.query.filter_by(id=id, type='1').first()

    def add(self, server):
        db.session.add(server)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).update({'type': '4'})  # 伪删除
        # self.query.filter_by(id=id).delete()
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
