from flask import render_template, abort
from flask_login import login_required, current_user

from . import admin
from app.models import *
from app import ethereum_service


@admin.route('/')
@login_required
def index():
    if not current_user.is_admin():
        abort(403)
    return render_template('admin/index.html')


@admin.route('/users')
@login_required
def users():
    if not current_user.is_admin():
        abort(403)
    users = User.query.all()
    for user in users:
        user.address = user.wallets[0].address
        user.balance = ethereum_service.to_ether(ethereum_service.get_balance(user.address))
    return render_template('admin/users.html', users=users)


@admin.route('/files')
@login_required
def files():
    if not current_user.is_admin():
        abort(403)
    return render_template('admin/files.html', files=File.query.order_by(File.time.desc()).all())


@admin.route('/authorizations')
@login_required
def authorizations():
    if not current_user.is_admin():
        abort(403)
    return render_template('admin/authorizations.html', authorizations=Authorization.query.all())


@admin.route('/transactions')
@login_required
def transactions():
    if not current_user.is_admin():
        abort(403)
    return render_template('admin/transactions.html', transactions=Transaction.query.all())
