from flask import jsonify, request, redirect, url_for, Response, abort, g
import models
from settings import app, db
from models import User
from flask_httpauth import HTTPTokenAuth
import logging
auth = HTTPTokenAuth(scheme='Bearer')


@app.route('/user/register', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        logging.INFO('missing arguments')
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        logging.INFO('user already exists')
        abort(400)  # existing user

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user:
        g.user = user
        return True
    else:
        return False


@app.route('/api/user/token', methods=['GET'])
def get_auth_token():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)
    u = User.query.filter_by(username=username).first()
    if u is None:
        print('no such user')
        abort(400)
    u.verify_password(password)
    token = u.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
