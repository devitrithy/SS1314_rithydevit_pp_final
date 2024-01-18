from flask import Blueprint

user_bp = Blueprint('users', __name__)

from routes.users import routes
