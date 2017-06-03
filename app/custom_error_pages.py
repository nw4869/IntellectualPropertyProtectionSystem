from flask import render_template


def request_error(e):
    return render_template('errors/400.html', e=e), 400


def forbidden(e):
    return render_template('errors/403.html', e=e), 403


def page_not_found(e):
    return render_template('errors/404.html', e=e), 404


def internal_server_error(e):
    return render_template('errors/500.html', e=e), 500


def balance_error(e):
    return render_template('errors/balance.html', e=e), 400


def ethereum_error(e):
    return request_error(e)