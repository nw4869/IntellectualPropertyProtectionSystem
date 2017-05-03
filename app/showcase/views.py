from flask import render_template
from flask_login import login_required

from . import showcase


@showcase.route('/')
@login_required
def index():
    return render_template('showcase/index.html')
