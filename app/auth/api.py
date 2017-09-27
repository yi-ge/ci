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
    def checkPathInAuth(path):
        noAuthDir = ['/public']
        for i in noAuthDir:
            if not request.path.startswith(i):
                return False
        return True

    @app.before_request
    def before_request():
        # ip = request.remote_addr
        # url = request.url
        # print (ip, url)
        if (request.method != 'OPTIONS'):
            if(not checkPathInAuth(request.path)):
                authResult = Auth.identify(Auth, request)
                if (authResult['status'] != 1):
                    return jsonify(authResult)
                else:
                    request.user = authResult['result']['data']

    @app.route('/public/auth/register', methods=['POST'])
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

    @app.route('/public/auth/login', methods=['POST'])
    def login():
        """
        User Login
        :return: json
        """
        content = request.get_json(silent=True) or request.form
        username = content['username']
        password = content['password']
        verfiycode = content['verfiycode']
        code = content['code']
        if (not code or not verficode):
            return jsonify(common.falseReturn(50100, '',
                                              'Please input identifying code'))
        if (redis.get('verfiy_' + code) and str(redis.get('verfiy_' + code), encoding="utf8").lower() != verfiycode.lower()):
            return jsonify(common.falseReturn(50101, '',
                                              'Identifying code error or time out'))
        if (not username or not password):
            return jsonify(common.falseReturn(50002, '',
                                              'Username and password cannot be empty'))
        else:
            return Auth.authenticate(Auth, username, password)

    @app.route('/auth/logout', methods=['GET'])
    def logout():
        """
        User Logout (Initiative)
        :return: json
        """

        redis.delete('user_' + str(request.user['userinfo']['id']))
        return jsonify(common.trueReturn('ok', 'Logouted'))

    @app.route('/public/auth/verfiycode', methods=['GET'])
    def verficode():
        """
        Verfiy Code
        :return: image/JPEG
        """
        image = create_validate_code()
        code = request.args.get('code')
        if (code):
            redis.set('verfiy_' + code, image[1], ex=60)
        res = Response()
        output = BytesIO()
        image[0].save(output, 'JPEG', quality=95)
        img_data = output.getvalue()
        res.headers.set("Content-Type", "image/JPEG;charset=UTF-8")
        res.set_data(img_data)
        output.close()
        return res

    @app.route('/public/auth/loginCheck', methods=['GET'])
    def loginCheck():
        """
        loginCheck
        :return: json
        """
        try:
            redis.set('check', 'redis', ex=60)
        except Exception as e:
            return jsonify(common.falseReturn(51100, '',
                                              'Redis error.'))

        if str(redis.get('check'), encoding="utf8") == "redis":
            return jsonify(common.trueReturn('ok', 'Pass'))

        return jsonify(common.falseReturn(51100, '', 'Server error.'))
