from flask import render_template, abort, current_app
from flask_login import login_required, current_user

import app
from app import File
from . import showcase


@showcase.route('/')
def index():
    return render_template('showcase/index.html')


@showcase.route('/<hash>')
def show_file(hash):
    file = File.query.filter_by(hash=hash).first()
    if file is None:
        abort(404)

    # TODO fix: file extension
    file_url = app.upload_files.url(file.hash+'.jpg')
    return render_template('showcase/file.html', file=file, file_url=file_url)