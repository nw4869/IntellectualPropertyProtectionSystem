from flask import Blueprint

ethereum = Blueprint('ethereum', __name__)

from . import views
