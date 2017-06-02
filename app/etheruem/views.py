from flask import render_template, abort, redirect, url_for
from datetime import datetime
import re

from app.etheruem import ethereum
from app.ethereum_service import get_transaction, get_block, get_block_by_tx, get_tx_distance, get_latest_block_number, get_latest_block


@ethereum.route('/blocks/latest')
def latest_block():
    blk = get_latest_block()
    blk['timestamp'] = datetime.fromtimestamp(blk['timestamp'])
    return render_template('ethereum/block.html', block=blk)


@ethereum.route('/blocks/<int:block_num>')
def block(block_num):
    if 0 > block_num or block_num > get_latest_block_number():
        abort(404)
    blk = get_block(block_num)
    if blk is None:
        abort(404)
    blk['timestamp'] = datetime.fromtimestamp(blk['timestamp'])
    return render_template('ethereum/block.html', block=blk)


@ethereum.route('/transactions/<tx_hash>')
def transaction(tx_hash):
    # if not tx_hash.startswith('0x'):
    #     return redirect(url_for('ethereum.transaction', tx_hash='0x' + tx_hash))

    if not re.match('0x[a-fA-F0-9]{64}', tx_hash):
        abort(404)

    tx = get_transaction(tx_hash)
    if tx is None:
        abort(404)
    tx['confirmations'] = get_tx_distance(tx_hash)
    return render_template('ethereum/transaction.html', tx=tx)
