from flask import render_template, abort, current_app, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc, and_

import app
from app import db
from . import showcase
from app import ethereum_service
from app.models import File, Transaction


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

    if not current_user.is_admin and not file.for_sell and file.owner_user != current_user:
        abort(403)

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
        abort(404)

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
    try:
        tx_hash = ethereum_service.purchase(current_user, file)
    except ethereum_service.EthereumException:
        abort(400, '购买失败')

    # 写入数据库
    transaction = Transaction(seller=file.owner, buyer=current_user.username, file_hash=file.hash, money=file.price,
                              txhash=tx_hash)
    db.session.add(transaction)

    return redirect(url_for('user.transactions'))
