import jwt, datetime, time
from flask import jsonify
from app.user.model import Users
from .. import config
from .. import common
from sqlalchemy import or_, not_

class Auth():
    @staticmethod
    def encode_auth_token(user_id, login_time):
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
                    'id': user_id,
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
            payload = jwt.decode(auth_token, config.SECRET_KEY, options={'verify_exp': False})
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
        userInfo = Users.query.filter(or_(Users.username==username, Users.phone==username, Users.email==username)).first()
        if (userInfo is None):
            return jsonify(common.falseReturn(50003, '', 'This user does not exist.'))
        else:
            if (Users.check_password(Users, userInfo.password, password)):
                login_time = int(time.time())
                userInfo.login_time = login_time
                Users.update(Users)
                token = self.encode_auth_token(userInfo.id, login_time)
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
                result = common.falseReturn(50101, '', 'Unknown authorization header.')
            else:
                auth_token = auth_tokenArr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user = Users.get(Users, payload['data']['id'])
                    if (user is None):
                        result = common.falseReturn(50005, '', 'This user does not exist.')
                    else:
                        if (user.login_time == payload['data']['login_time']):
                            result = common.trueReturn(user.id, 'Pass Request')
                        else:
                            result = common.falseReturn(50102, '', 'Token has been changed, please request again.')
                else:
                    result = common.falseReturn(50103, '', payload)
        else:
            result = common.falseReturn(50104, '', ' Authentication required. Token not found.')
        return result
