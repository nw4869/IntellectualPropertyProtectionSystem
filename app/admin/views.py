from flask import render_template, abort
from flask_login import login_required, current_user

from . import admin
from app.models import *


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
    return render_template('admin/users.html', users=User.query.all())


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
