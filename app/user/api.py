from flask import jsonify, request, Response
from app.user.model import Users
from app.auth.auths import Auth
from sqlalchemy import or_, not_
from .. import common
from io import BytesIO, StringIO
from app.user.validate_code import create_validate_code
from app.redis import r
import os

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
        if (request.method != 'OPTIONS'):
            if(not checkPathInAuth(request.path)):
                authResult = Auth.identify(Auth, request)
                if (authResult['status'] != 1):
                    return jsonify(authResult)


    @app.route('/public/register', methods=['POST'])
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
            return jsonify(common.falseReturn(50100, '', 'Please input identifying code'))
        if (str(r.get('verfiy_' + code), encoding = "utf8").lower() != verfiycode.lower()):
            return jsonify(common.falseReturn(50101, '', 'Identifying code error or time out'))
        if (username and password and phone and email):
            user = Users(email=email, phone=phone, username=username, password=Users.set_password(Users, password))
            result = Users.add(Users, user)
            if user.id:
                return Auth.authenticate(Auth, username, password)
            else:
                return jsonify(common.falseReturn(50001, '', '用户注册失败'))
        else:
            return jsonify(common.falseReturn(50020, '', '缺少必须参数'))

    @app.route('/public/login', methods=['POST'])
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
            return jsonify(common.falseReturn(50100, '', 'Please input identifying code'))
        if (str(r.get('verfiy_' + code), encoding = "utf8").lower() != verfiycode.lower()):
            return jsonify(common.falseReturn(50101, '', 'Identifying code error or time out'))
        if (not username or not password):
            return jsonify(common.falseReturn(50002, '', 'Username and password cannot be empty'))
        else:
            return Auth.authenticate(Auth, username, password)

    @app.route('/logout', methods=['POST'])
    def logout():
        """
        User Logout
        :return: json
        """
        content = request.get_json(silent=True) or request.form
        username = content['username']
        if (str(r.get('verfiy_' + code), encoding = "utf8").lower() != verfiycode.lower()):
            return jsonify(common.falseReturn(50101, '', 'Identifying code error or time out'))
        if (not username):
            return jsonify(common.falseReturn(50002, '', 'Username and password cannot be empty'))
        else:
            return Auth.authenticate(Auth, username, password)

    @app.route('/public/verfiycode', methods=['GET'])
    def verficode():
        """
        Verfiy Code
        :return: image/JPEG
        """
        # codenum = 4
        # source = list()
        # for index in range(0, 10):
        #     source.append(str(index))
        # code = ''.join(random.sample(source, 4))
        image = create_validate_code(font_type=os.path.dirname(os.path.realpath(__file__)) + "/angelina.ttf")
        code = request.args.get('code')
        if (code):
            r.set('verfiy_' + code, image[1], ex=60)
        res = Response()
        output = BytesIO()
        print(image[1])
        image[0].save(output, 'JPEG', quality = 95)
        img_data = output.getvalue()
        res.headers.set("Content-Type", "image/JPEG;charset=UTF-8")
        res.set_data(img_data)
        output.close()
        return res


    @app.route('/user', methods=['GET'])
    def get():
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
        user = Users.query.filter(or_(Users.phone==value, Users.username==value, Users.email==value)).first()
        if (user is None):
            result = common.trueReturn('', "OK")
        else:
            result = common.falseReturn(2, '', "The " + content['type'] + " is registered")

        return jsonify(result)
