import jwt
import datetime
import time
from flask import jsonify
from app.user.model import Users
from .. import config
from .. import common
from sqlalchemy import or_, not_
from app.redis import redis


class Auth():
    @staticmethod
    def encode_auth_token(userinfo, login_time):
        """
        Encode token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'userinfo': jsonify(userinfo),
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decode Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, config.SECRET_KEY, options={
                                 'verify_exp': False})
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Expire Token'
        except jwt.InvalidTokenError:
            return 'Invalid Token'

    def authenticate(self, username, password):
        """
        User Login Authenticate
        :param password:
        :return: json
        """
        userInfo = Users.query.filter(or_(
            Users.username == username, Users.phone == username, Users.email == username)).first()
        if (userInfo is None):
            return jsonify(common.falseReturn(50003, '', 'This user does not exist.'))
        else:
            if (Users.check_password(Users, userInfo.password, password)):
                login_time = int(time.time())
                userInfo.login_time = login_time
                Users.update(Users)
                UnReadMsg = userInfo
                print(UnReadMsg.__dict__)
                token = self.encode_auth_token(userInfo, login_time)
                # print(userInfo)
                # redis.set('user_' + str(userInfo.id), jsonify({
                #     'userinfo': jsonify(userInfo),
                #     'login_time': login_time
                # }), ex=3600 * 24 * 7)
                return jsonify(common.trueReturn({'token': token.decode()}, 'Successful authentication.'))
            else:
                return jsonify(common.falseReturn(50004, '', 'Sorry, wrong password, please login again.'))

    def identify(self, request):
        """
        Identify
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if (auth_header):
            auth_tokenArr = auth_header.split(" ")
            if (not auth_tokenArr or auth_tokenArr[0] != 'Bearer' or len(auth_tokenArr) != 2):
                result = common.falseReturn(
                    50101, '', 'Unknown authorization header.')
            else:
                auth_token = auth_tokenArr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user = redis.get('user_' + payload['data']['userinfo']['id'])
                    if (user):
                        if (user.login_time == payload['data']['userinfo']['login_time']):
                            result = common.trueReturn(user, 'Pass Request')
                        else:
                            result = common.falseReturn(
                                50102, '', 'Token has been changed, please request again.')
                    else:
                        result = common.falseReturn(
                            50005, '', 'This user does not exist.')
                else:
                    result = common.falseReturn(50103, '', payload)
        else:
            result = common.falseReturn(
                50104, '', ' Authentication required. Token not found.')
        return result
