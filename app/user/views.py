from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy import or_

from app import File
from . import user
from app.models import *


@user.route('/')
def index():
    return render_template('user/index.html')


@user.route('/files')
@login_required
def files():
    return render_template('user/files.html', files=current_user.files)


@user.route('/transactions')
@login_required
def transactions():
    return render_template(
        'user/transactions.html',
        files=Transaction.query.filter(
            or_(Transaction.buyer_user == current_user, Transaction.seller_user == current_user))
            .order_by(Transaction.time.desc()).all()
    )


@user.route('/authorizations')
@login_required
def authorizations():
    return render_template(
        'user/authorizations.html',
        files=Authorization.query.filter(
            or_(Authorization.authorizer_user == current_user, Authorization.authorizer_user == current_user))
            .order_by(Authorization.time.desc()).all()
    )
