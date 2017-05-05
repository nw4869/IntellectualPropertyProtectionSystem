from flask import render_template, current_app, url_for
from flask_login import login_required, current_user
from sha3 import keccak_256
from werkzeug.utils import secure_filename, redirect
from datetime import datetime

from . import main
from .forms import UploadForm
from app import db
import app
from app.ethereum import submit_file
from app.models import File


@main.route('/')
def index():
    current_app.logger.info("info test")
    return render_template('index.html')


@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        hash = keccak_256(form.file.data.stream.read()).hexdigest()
        filename = form.filename.data
        description = form.description.data

        file = File(hash=hash, filename=filename, description=description)
        # file.owner_user = current_user
        file.owner = current_user.username
        # file.time = datetime.now()
        file.txhash = submit_file(file)
        db.session.add(file)
        # print(file)

        # reset stream index
        form.file.data.stream.seek(0)
        saved_filename = app.upload_files.save(form.file.data, name=hash + '.')
        file_url = app.upload_files.url(saved_filename)
        return redirect(url_for('showcase.show_file', hash=file.hash))
    else:
        file_url = None
    return render_template('upload.html', form=form, file_url=file_url)
