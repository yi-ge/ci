from flask import jsonify, request, Response
from app.server.model import Server
from app.auth.auths import Auth
from sqlalchemy import or_, not_
from .. import common
from io import BytesIO, StringIO
from app.utils.validate_code.main import create_validate_code
from app.redis import redis
from app.utils.serializer.sqlalchemy_json import Serializer

validata_code = StringIO()


def init_api(app):

    @app.route('/server/list', methods=['GET', 'POST'])
    def test():
        """
        Get Server List
        :return: json
        """
        servers = Server.query.filter_by(type='1').all()

        lists = []
        for server in servers:
            lists.append(Serializer.serialize(server))

        result = common.trueReturn(lists, "请求成功")
        return jsonify(result)

    @app.route('/server/add', methods=['POST'])
    def addServer():
        """
        Server Add
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
        status = content['status']
        if (name and ip and auth and status):
            server = Server(name=name, ip=ip, auth=auth, sshkey=sshkey, password=password, address=address, note=note, status=status, type='1')
            result = Server.add(Server, server)
            if server.id:
                return jsonify(common.trueReturn(request.user, "Save Ok"))
            else:
                return jsonify(common.falseReturn(50001, '', 'Fail'))
        else:
            return jsonify(common.falseReturn(50020, '', 'The parameters are necessary.'))

    @app.route('/server/del', methods=['POST'])
    def delServer():
        """
        Server Delete
        :return: json
        """
        content = request.get_json(silent=True) or request.form
        id = content['id']
        if id:
            Server.delete(Server, id)
            return jsonify(common.trueReturn('ok', "Save Ok"))
        else:
            return jsonify(common.falseReturn(50020, '', 'The parameters are necessary.'))
