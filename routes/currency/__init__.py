from flask import Blueprint

currency_bp = Blueprint('currency', __name__)

from routes.currency import routes
