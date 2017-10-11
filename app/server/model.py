from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(250),  unique=True, nullable=False)
    auth = db.Column(db.String(15),  unique=True, nullable=False)
    sshkey = db.Column(db.String(2096),  unique=True, nullable=False)
    password = db.Column(db.String(250))
    note = db.Column(db.Text)

    def __init__(self, ip, auth, sshkey, password, note):
        self.ip = ip
        self.auth = auth
        self.sshkey = sshkey
        self.password = password
        self.note = note

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
