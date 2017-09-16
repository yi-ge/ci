from flask import jsonify, request
from app.user.model import Users
from app.auth.auths import Auth
from sqlalchemy import or_, not_
from .. import common

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
        print(email, phone, username, password)
        if (username and password and phone and email):
            user = Users(email=email, phone=phone, username=username, password=Users.set_password(Users, password))
            result = Users.add(Users, user)
            if user.id:
                returnUser = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'phone': user.phone,
                    'login_time': user.login_time
                }
                return jsonify(common.trueReturn(returnUser, "用户注册成功"))
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
        if (not username or not password):
            return jsonify(common.falseReturn(50002, '', '用户名和密码不能为空'))
        else:
            return Auth.authenticate(Auth, username, password)


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
        if (content['type'] == 'phone'):
            phone = content['phone']
            user = Users.query.filter(or_(Users.phone==phone, Users.username==phone, Users.email==phone)).first()
            if (user is None):
                result = common.trueReturn('', "Ok")
            else:
                result = common.falseReturn(2, '', "The phone is registered")
        elif (content['type'] == 'email'):
            email = content['email']
            user = Users.query.filter(or_(Users.phone==email, Users.username==email, Users.email==email)).first()
            if (user is None):
                result = common.trueReturn('', "OK")
            else:
                result = common.falseReturn(2, '', "The email is registered")
        elif (content['type'] == 'username'):
            username = content['username']
            user = Users.query.filter(or_(Users.phone==username, Users.username==username, Users.email==username)).first()
            if (user is None):
                result = common.trueReturn('', "OK")
            else:
                result = common.falseReturn(2, '', "The username is registered")

        return jsonify(result)
