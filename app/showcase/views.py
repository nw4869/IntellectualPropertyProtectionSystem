from flask import render_template, abort, current_app
from flask_login import login_required, current_user
from sqlalchemy import desc

import app
from app import File
from . import showcase


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

    if not file.for_sell and file.owner_user != current_user:
        abort(403)

    # TODO fix: file extension
    file_url = app.upload_files.url(file.hash+'.jpg')
    return render_template('showcase/file.html', file=file, file_url=file_url)