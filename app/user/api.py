from flask import jsonify, request
from app.user.model import Users
from app.auth.auths import Auth
from .. import common

def init_api(app):
    @app.route('/register', methods=['POST'])
    def register():
        """
        用户注册
        :return: json
        """
        email = request.form.get('email')
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
        用户登录
        :return: json
        """
        username = request.form.get('username')
        password = request.form.get('password')
        if (not username or not password):
            return jsonify(common.falseReturn(50002, '', '用户名和密码不能为空'))
        else:
            return Auth.authenticate(Auth, username, password)


    @app.route('/user', methods=['GET'])
    def get():
        """
        获取用户信息
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
        content = request.get_json(silent=True)
        result = {}
        if (content['type'] == 'phone'):
            phone = content['phone']
            user = Users.query.filter_by(phone=phone).first()
            if (user is None):
                result = common.trueReturn('', "请求成功")
            else:
                result = common.falseReturn(2, '', "手机号已存在")
        elif (content['type'] == 'email'):
            email = content['email']
            user = Users.query.filter_by(email=email).first()
            if (user is None):
                result = common.trueReturn('', "请求成功")
            else:
                result = common.falseReturn(2, '', "Email已存在")
        elif (content['type'] == 'username'):
            username = content['username']
            user = Users.query.filter_by(username=username).first()
            if (user is None):
                result = common.trueReturn('', "请求成功")
            else:
                result = common.falseReturn(2, '', "用户名已存在")

        return jsonify(result)
