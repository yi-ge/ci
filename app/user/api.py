from flask import jsonify, request, Response
from app.user.model import Users
from app.auth.auths import Auth
from sqlalchemy import or_, not_
from .. import common
from io import BytesIO, StringIO
from app.utils.validate_code.main import create_validate_code
from app.redis import redis

validata_code = StringIO()


def init_api(app):

    @app.route('/userinfo', methods=['POST'])
    def userinfo():
        """
        Get User Info
        :return: json
        """
        result = Auth.identify(Auth, request)
        if (result['status'] and result['data']):
            user = Users.get(Users, result['data'])
            returnUser = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'login_time': user.login_time
            }
            result = common.trueReturn(returnUser, "请求成功")
        return jsonify(result)

    @app.route('/public/user/dereplication', methods=['POST'])
    def dereplication():
        """
        Dereplication
        :return: json
        """
        content = request.get_json(silent=True) or request.form
        result = {}
        value = content['value']
        user = Users.query.filter(
            or_(Users.phone == value, Users.username == value, Users.email == value)).first()
        if (user is None):
            result = common.trueReturn('', "OK")
        else:
            result = common.falseReturn(
                2, '', "The " + content['type'] + " is registered")

        return jsonify(result)
