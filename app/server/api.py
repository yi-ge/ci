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
        name = content['name']
        ip = content['ip']
        auth = content['auth']
        sshkey = content['sshkey']
        password = content['password']
        address = content['address']
        note = content['note']
        if (name and ip and auth):
            server = Server(name=name, ip=ip, auth=auth, sshkey=sshkey, password=password, address=address, note=note)
            result = Server.add(Server, server)
            if server.id:
                return common.trueReturn(request.user, "Save Ok")
            else:
                return jsonify(common.falseReturn(50001, '', 'Fail'))
        else:
            return jsonify(common.falseReturn(50020, '', 'The parameters are necessary.'))
