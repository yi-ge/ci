from flask import jsonify, request, Response
from app.server.model import Server
from app.auth.auths import Auth
from sqlalchemy import or_, not_
from .. import common
from io import BytesIO, StringIO
from app.utils.validate_code.main import create_validate_code
from app.redis import redis

validata_code = StringIO()


def init_api(app):

    @app.route('/server/list', methods=['POST'])
    def test():
        """
        Get Server List
        :return: json
        """
        result = common.trueReturn(request.user, "请求成功")
        return jsonify(result)

    @app.route('/server/add', methods=['POST'])
    def register():
        """
        User Register
        :return: json
        """
        content = request.get_json(silent=True) or request.form
        email = content['email']
        phone = content['phone']
        username = content['username']
        password = content['password']
        verfiycode = content['verfiycode']
        code = content['code']
        if (not code or not verficode):
            return jsonify(common.falseReturn(50100, '',
                                              'Please input identifying code'))
        if (str(redis.get('verfiy_' + code), encoding="utf8").lower() != verfiycode.lower()):
            return jsonify(common.falseReturn(50101, '',
                                              'Identifying code error or time out'))
        if (username and password and phone and email):
            user = User(email=email, phone=phone, username=username,
                        password=User.set_password(User, password))
            result = User.add(User, user)
            if user.id:
                return Auth.authenticate(Auth, username, password)
            else:
                return jsonify(common.falseReturn(50001, '', '用户注册失败'))
        else:
            return jsonify(common.falseReturn(50020, '', '缺少必须参数'))
