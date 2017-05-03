from flask import render_template, request
from . import main


@main.route('/')
def index():
    return render_template('index.html')
