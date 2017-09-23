from flask import jsonify, request, Response
from app.user.model import User
from app.auth.auths import Auth
from sqlalchemy import or_, not_
from .. import common
from io import BytesIO, StringIO
from app.utils.validate_code.main import create_validate_code
from app.redis import redis

validata_code = StringIO()


def init_api(app):

    @app.route('/user/info', methods=['POST'])
    def userinfo():
        """
        Get User Info
        :return: json
        """
        result = common.trueReturn(request.user, "请求成功")
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
        user = User.query.filter(
            or_(User.phone == value, User.username == value, User.email == value)).first()
        if (user is None):
            result = common.trueReturn('', "OK")
        else:
            result = common.falseReturn(
                2, '', "The " + content['type'] + " is registered")

        return jsonify(result)
