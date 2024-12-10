from flask import Blueprint

mypage_bp = Blueprint('mypage', __name__, template_folder='../templates')

from . import routes