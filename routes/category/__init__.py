from flask import Blueprint

category_bp = Blueprint('category', __name__)

from routes.category import routes
