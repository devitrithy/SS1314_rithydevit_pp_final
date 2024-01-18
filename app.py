from random import randint
from routes.products import product_bp
from routes.users import user_bp
from routes.currency import currency_bp
from routes.customers import customer_bp
from routes.category import category_bp

import names
from flask import Flask,  render_template, request,session

app = Flask(__name__)


@app.route('/')
def home():
    category = ["All", "Drink", "Food", "Beer", "Energy Drink"]
    active = request.args.get('category')
    products = []
    for i in range(15):
        products.append({
            "id": i,
            "name": names.get_full_name(),
            "old_price": randint(5, 10),
            "discount": randint(5, 25),
            "description": names.get_full_name(),
            "category": category[randint(1, 4)]
        })
    product_filter = []
    print(active)
    if active == "All" or active is None:
        product_filter = products
        active = "All"
    else:
        for p in products:
            if active == p['category']:
                product_filter.append(p)

    return render_template("index.html", products=product_filter, categories=category, active=active)


@app.route("/detail/<id>")
def detail(id):
    return render_template("detail.html", id=id)


@app.route("/admin")
def admin():
    current_url = "/admin"
    return render_template("admin/index.html", url=current_url)



@app.errorhandler(404)
def error_404(e):
    return render_template("404.html")


@app.errorhandler(500)
def error_500(e):
    return render_template("500.html")


app.register_blueprint(product_bp)
app.register_blueprint(category_bp)
app.register_blueprint(user_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(currency_bp)

if __name__ == '__main__':
    app.run()
