from flask import render_template


def forbidden(e):
    return render_template('403.html'), 403


def page_not_found(e):
    return render_template('404.html'), 404


def internal_server_error(e):
    return render_template('500.html'), 500
