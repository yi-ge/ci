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
