from flask import render_template


def request_error(e):
    return render_template('400.html', e=e), 400


def forbidden(e):
    return render_template('403.html', e=e), 403


def page_not_found(e):
    return render_template('404.html', e=e), 404


def internal_server_error(e):
    return render_template('500.html', e=e), 500
