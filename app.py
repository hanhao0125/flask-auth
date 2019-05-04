from flask import jsonify, request, redirect, url_for, Response

import models
from settings import app, db
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user

login_manager = LoginManager()
# login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)


@login_manager.user_loader
def load_user(id):
    try:
        return models.User.query.get(int(id))
    except IndexError:
        return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        user = models.User.query.filter(models.User.account == account).first()
        if user is not None:
            if user.verify_password(password):
                # user = models.User(account)
                login_user(user)
                return jsonify('success')
            else:
                return jsonify('密码不正确！')
        else:
            return jsonify('账号不存在')


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        print(account, password)
        user = models.User.query.filter(models.User.account == account).first()
        if user is not None:
            return jsonify('用户名已存在！')
        else:
            user = models.User(account)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            print(user)
        return jsonify('success')


@app.route('/')
@app.route('/main')
@login_required
def main():
    return jsonify('main')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify('success logout')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
