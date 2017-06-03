from flask import render_template, abort, current_app, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc, and_

import app
from app import db
from app.errors import EthereumException
from . import showcase
from app import ethereum_service
from app.models import File, Transaction, Authorization, User


@showcase.route('/')
def index():
    files = File.query.filter_by(for_sell=True).order_by(desc(File.time)).all()
    for file in files:
        # TODO: file extension
        file.url = app.upload_files.url(file.hash + '.jpg')
    return render_template('showcase/index.html', files=files)


@showcase.route('/<hash>')
def show_file(hash):
    file = File.query.filter_by(hash=hash).first()
    if file is None:
        abort(404)

    if not file.for_sell:
        if not current_user.is_authenticated:
            abort(403, '请先登录')
        elif not current_user.is_admin() and file.owner_user != current_user:
            authorization = file.authorizations.filter_by(authorized_user=current_user).first()
            if authorization is None:
                abort(403)
            elif not ethereum_service.tx_is_confirmed(authorization.txhash):
                abort(403, '请等待授权完成')

    # TODO fix: file extension
    file_url = app.upload_files.url(file.hash + '.jpg')
    file.is_confirmed = ethereum_service.file_is_confirmed(file)
    file.confirm_num = ethereum_service.get_tx_distance(file.txhash)
    return render_template('showcase/file.html', file=file, file_url=file_url)


@showcase.route('/<hash>/purchase', methods=['POST'])
@login_required
def purchase(hash):
    file = File.query.filter_by(hash=hash).first()
    if file is None:
        abort(404, '文件不存在')

    if not ethereum_service.file_is_confirmed(file):
        abort(400, '作品尚未确认，不能购买')

    # 不能购买自己的
    if file.owner_user == current_user:
        abort(400, '不能购买自己的作品')

    if Transaction.query.filter(and_(Transaction.file == file, Transaction.buyer_user == current_user)).first():
        abort(400, '已经购买')

    # 不能购买未出售的
    if not file.for_sell:
        abort(403, '该作品未出售')

    # 检查余额
    balance = ethereum_service.to_ether(ethereum_service.get_balance(current_user.wallets[0].address))
    if balance < file.price:
        abort(400, '余额不足')

    # 写入以太坊
    tx_hash = ethereum_service.purchase(current_user, file)

    # 写入数据库
    transaction = Transaction(seller=file.owner, buyer=current_user.username, file_hash=file.hash, money=file.price,
                              txhash=tx_hash)
    db.session.add(transaction)

    return redirect(url_for('user.transactions'))


@showcase.route('/<hash>/authorize/<to_user>', methods=['POST'])
@login_required
def authorize(hash, to_user):
    file = File.query.filter_by(hash=hash).first()
    if file is None:
        abort(404, '文件不存在')

    to_user_entity = User.query.filter_by(username=to_user).first()
    if not to_user_entity:
        abort(400, '用户名有误')

    # 只能授权自己的的作品
    if file.owner_user != current_user:
        abort(403, '只能授权自己的作品')

    if not ethereum_service.file_is_confirmed(file):
        abort(400, '作品尚未确认，不能授权')

    if Authorization.query.filter(
            and_(Authorization.file == file, Authorization.authorized_username == to_user)).first():
        abort(400, '该用户已经授权')

    # 写入以太坊
    tx_hash = ethereum_service.authorize(current_user, to_user_entity, file)

    # 写入数据库
    authorization = Authorization(file_hash=file.hash, authorizer_username=current_user.username,
                                  authorized_username=to_user,
                                  txhash=tx_hash)
    db.session.add(authorization)

    return redirect(url_for('user.authorizations'))
