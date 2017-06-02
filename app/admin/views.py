from flask import render_template, abort
from flask_login import login_required, current_user

from app.decorators import admin_required
from . import admin
from app.models import *
from app import ethereum_service


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/users')
@admin_required
def users():
    users = User.query.all()
    for user in users:
        user.address = user.wallets[0].address
        user.balance = ethereum_service.to_ether(ethereum_service.get_balance(user.address))
    return render_template('admin/users.html', users=users)


@admin.route('/files')
@admin_required
def files():
    return render_template('admin/files.html', files=File.query.order_by(File.time.desc()).all())


@admin.route('/authorizations')
@admin_required
def authorizations():
    return render_template('admin/authorizations.html', authorizations=Authorization.query.all())


@admin.route('/transactions')
@admin_required
def transactions():
    return render_template('admin/transactions.html', transactions=Transaction.query.all())
