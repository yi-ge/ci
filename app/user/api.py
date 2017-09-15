from flask import jsonify, request
from app.user.model import Users
from app.auth.auths import Auth
from .. import common

def init_api(app):
    @app.route('/register', methods=['POST'])
    def register():
        """
        User Register
        :return: json
        """
        email = request.form.get('email')
        phone = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users(email=email, username=username, password=Users.set_password(Users, password))
        result = Users.add(Users, user)
        if user.id:
            returnUser = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'login_time': user.login_time
            }
            return jsonify(common.trueReturn(returnUser, "用户注册成功"))
        else:
            return jsonify(common.falseReturn(50001, '', '用户注册失败'))


    @app.route('/login', methods=['POST'])
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
            user = Users.query.filter_by(phone=phone).first()
            if (user is None):
                result = common.trueReturn('', "Ok")
            else:
                result = common.falseReturn(2, '', "The phone is registered")
        elif (content['type'] == 'email'):
            email = content['email']
            user = Users.query.filter_by(email=email).first()
            if (user is None):
                result = common.trueReturn('', "OK")
            else:
                result = common.falseReturn(2, '', "The email is registered")
        elif (content['type'] == 'username'):
            username = content['username']
            user = Users.query.filter_by(username=username).first()
            if (user is None):
                result = common.trueReturn('', "OK")
            else:
                result = common.falseReturn(2, '', "The username is registered")

        return jsonify(result)
