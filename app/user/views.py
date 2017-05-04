from flask import render_template
from flask_login import login_required

from . import user


@user.route('/')
def index():
    return render_template('user/index.html')
