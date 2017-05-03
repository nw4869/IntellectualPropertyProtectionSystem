from flask import Blueprint

showcase = Blueprint('showcase', __name__)

from . import views
