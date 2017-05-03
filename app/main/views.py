from flask import render_template, request
from flask_login import login_required
from . import main


@main.route('/')
def index():
    return render_template('index.html')

@login_required
@main.route('/upload')
def upload():
    return render_template('upload.html')
