from flask import Blueprint

customer_bp = Blueprint('customers', __name__)

from routes.customers import routes
