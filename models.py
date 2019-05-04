from settings import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(128))
    register_date = db.Column(db.DateTime)
    email = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    is_admin = db.Column(db.Boolean)

    def __init__(self, account):
        self.username = account
        self.account = account
        self.register_date = datetime.utcnow()
        self.is_admin = False

    def hash_password(self, password):
        self.password = generate_password_hash(password)
        return self.password

    def verify_password(self, password):
        password_hash = generate_password_hash(password)
        if password_hash is None:
            return False
        return check_password_hash(self.password, password)

    def admin(self):
        return self.is_admin

    def __repr__(self):
        return 'User name=%s' % self.username


def import_user():
    for i in range(1000, 3000, 3):
        user = User('jobs' + str(i) + '@gmail.com')
        user.hash_password('1')
        user.email = 'jobs' + str(i) + '@gmail.com'
        user.phone = '1786678' + str(i)
        db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    db.session.commit()
    import_user()
