from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from app import db
from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.args.get('next'):
        form.next.data = request.args.get('next')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(form.next.data or url_for('main.index'))
        form.password.errors.append('账号密码错误')
        # flash('账号密码错误')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('登出成功')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.args.get('next'):
        form.next.data = request.args.get('next')
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, name=form.name.data)
        db.session.add(user)
        flash('注册成功, 请登录')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)