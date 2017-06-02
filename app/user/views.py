from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy import or_

from app import File
from app.user.forms import TransferForm
from . import user
from app.models import *
from app.ethereum_service import get_balance, to_ether
from app import ethereum_service


@user.route('/')
def index():
    return render_template('user/index.html')


@user.route('/wallet', methods=['GET', 'POST'])
@login_required
def wallet():
    user_wallet = current_user.wallets[0]
    user_wallet.balance = to_ether(get_balance(user_wallet.address))

    form = TransferForm()
    if form.validate_on_submit():
        money = ethereum_service.to_wei(form.value.data)
        tx_hash = ethereum_service.transfer(_from=user_wallet.address, to=form.to.data, value=money)
        form = TransferForm()
        return render_template('user/wallet.html', wallet=user_wallet, tx_hash=tx_hash, form=form)

    return render_template('user/wallet.html', wallet=user_wallet, form=form)


@user.route('/files')
@login_required
def files():
    return render_template('user/files.html', files=current_user.files)


@user.route('/transactions')
@login_required
def transactions():
    return render_template(
        'user/transactions.html',
        transactions=Transaction.query.filter(
            or_(Transaction.buyer_user == current_user, Transaction.seller_user == current_user))
            .order_by(Transaction.time.desc()).all()
    )


@user.route('/authorizations')
@login_required
def authorizations():
    return render_template(
        'user/authorizations.html',
        authorizations=Authorization.query.filter(
            or_(Authorization.authorizer_user == current_user, Authorization.authorizer_user == current_user))
            .order_by(Authorization.time.desc()).all()
    )
