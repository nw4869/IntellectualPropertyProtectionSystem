from flask import render_template
from flask_login import login_required

from . import admin


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/users')
@login_required
def users():
    return render_template('admin/users.html')


@admin.route('/files')
@login_required
def files():
    return render_template('admin/files.html')


@admin.route('/authorizations')
@login_required
def authorizations():
    return render_template('admin/authorizations.html')


@admin.route('/transactions')
@login_required
def transactions():
    return render_template('admin/transactions.html')
