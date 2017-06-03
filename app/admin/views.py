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
    files = File.query.order_by(File.time.desc()).all()
    for file in files:
        file.is_confirmed = ethereum_service.file_is_confirmed(file)
        file.confirm_num = ethereum_service.get_tx_distance(file.txhash)
    return render_template('admin/files.html', files=files)


@admin.route('/authorizations')
@admin_required
def authorizations():
    authorizations = Authorization.query.all()
    append_confirm_info(authorizations)
    return render_template('admin/authorizations.html', authorizations=authorizations)


@admin.route('/transactions')
@admin_required
def transactions():
    transactions = Transaction.query.all()
    append_confirm_info(transactions)
    return render_template('admin/transactions.html', transactions=transactions)


def append_confirm_info(_list):
    for item in _list:
        item.is_confirmed = ethereum_service.tx_is_confirmed(item.txhash)
        item.confirm_num = ethereum_service.get_tx_distance(item.txhash)
    return _list
