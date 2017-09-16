from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from auth import Auth

db = SQLAlchemy()

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    @app.before_request
    def before_request():
        if (request.method != 'OPTIONS'):
            print('content')
            Auth.identify(Auth, request)

    @app.after_request
    def after_request(response):
        # CORS
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, DNT,User-Agent, Keep-Alive, Origin, X-Requested-With, Content-Type, Accept,x-clientid'
        return response

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'status': 400, 'result': {'msg': 'Bad request.'}}), 400

    @app.errorhandler(404)
    def bad_request(e):
        return jsonify({'status': 404, 'result': {'msg': 'This api does not exist.'}}), 404

    @app.errorhandler(500)
    def bad_request(e):
        return jsonify({'status': 400, 'result': {'msg': 'Internal server error.'}}), 500

    from app.user.model import db
    db.init_app(app)

    from app.user.api import init_api
    init_api(app)

    return app
