from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    ip = db.Column(db.String(35), unique=True, nullable=False)
    auth = db.Column(db.String(14), nullable=False)
    sshkey = db.Column(db.String(2096), nullable=True)
    password = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    note = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(250), nullable=True, nullable=False)

    def __init__(self, name, ip, auth, sshkey, password, address, note, status):
        self.name = name
        self.ip = ip
        self.auth = auth
        self.sshkey = sshkey
        self.password = password
        self.address = address
        self.note = note
        self.status = status

    def __str__(self):
        return "Server(id='%s')" % self.id

    def get(self, id):
        return self.query.filter_by(id=id).first()

    def add(self, server):
        db.session.add(server)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
