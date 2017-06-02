from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import login_manager
from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    username = db.Column(db.String(255), primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Integer, default=0, nullable=False)

    # buy_transactions = db.relationship('Transaction', back_populates='buyer_user', lazy='dynamic',
    #                                    cascade="all, delete-orphan", )
    # sell_transactions = db.relationship('Transaction', back_populates='seller_user', lazy='dynamic',
    #                                     cascade="all, delete-orphan")

    files = db.relationship('File', backref='owner_user', lazy='dynamic', cascade="all, delete-orphan")
    wallets = db.relationship('Wallet', backref='owner_user', lazy='dynamic', cascade="all, delete-orphan")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_admin(self):
        return self.role > 0

    # for flask-login
    def is_active(self):
        return self.role != -1

    # for flask-login
    def get_id(self):
        return self.username


class AnonymousUserMixin(AnonymousUserMixin):
    def is_admin(self):
        return False

login_manager.anonymous_user = AnonymousUserMixin


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    buyer = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    txhash = db.Column(db.String(255), nullable=False)
    money = db.Column(db.Float, nullable=False)
    time = db.Column(db.TIMESTAMP, default=db.func.now(), nullable=False)
    file_hash = db.Column(db.String(255), db.ForeignKey('files.hash'), nullable=False)

    buyer_user = db.relationship('User',
                                 backref=db.backref('buy_transactions', lazy='dynamic', cascade="all, delete-orphan"),
                                 foreign_keys=[buyer], uselist=False)
    seller_user = db.relationship('User',
                                  backref=db.backref('sell_transactions', lazy='dynamic', cascade="all, delete-orphan"),
                                  foreign_keys=[seller], uselist=False)


class File(db.Model):
    __tablename__ = 'files'
    hash = db.Column(db.String(255), primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    time = db.Column(db.TIMESTAMP, default=db.func.now(), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    owner = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    txhash = db.Column(db.String(255), nullable=False)
    for_sell = db.Column(db.Boolean, nullable=False, default=False)
    price = db.Column(db.Float, nullable=True)

    transactions = db.relationship('Transaction', backref='file', lazy='dynamic', cascade="all, delete-orphan")
    authorizations = db.relationship('Authorization', backref='file', lazy='dynamic', cascade="all, delete-orphan")

    def __str__(self):
        return '<File %r>' % self.hash


class Authorization(db.Model):
    __tablename__ = 'authorizations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_hash = db.Column(db.String(255), db.ForeignKey('files.hash'), nullable=False)
    authorizer_username = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    authorized_username = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    type = db.Column(db.Integer, default=0, nullable=False)
    time = db.Column(db.TIMESTAMP, default=db.func.now(), nullable=False)
    txhash = db.Column(db.String(255), nullable=False)

    authorizer_user = db.relationship('User', backref='authorizer_authorizations', foreign_keys=[authorizer_username])
    authorized_user = db.relationship('User', backref='authorized_authorizations', foreign_keys=[authorized_username])


class Wallet(db.Model):
    __tablename__ = 'wallets'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    key = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    owner = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
