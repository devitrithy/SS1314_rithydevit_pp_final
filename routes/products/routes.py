import sqlite3

import uuid
from flask import render_template, request, redirect
from dotenv import load_dotenv
import os
from routes.products import product_bp

load_dotenv()

TRUE = os.environ.get('true_code')
FALSE = os.environ.get('false_code')
CREATE = os.environ.get('create_code')
UPDATE = os.environ.get('update_code')
DELETE = os.environ.get('delete_code')

app = product_bp


@app.route("/admin/product")
def product():
    succeeded = ''
    type_name = 0
    success = request.args.get("success")
    type = request.args.get("type")
    if success == TRUE:
        succeeded = True
    if success == FALSE:
        succeeded = False
    if type == CREATE:
        type_name = 1
    elif type == UPDATE:
        type_name = 2
    elif type == DELETE:
        type_name = 3
    else:
        type_name = 0

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * from product;")
    products = cur.fetchall()
    current_url = "/admin/product"
    return render_template("admin/product/index.html", url=current_url, products=products, success=succeeded,
                           type=type_name)


@app.route("/admin/product/add")
def add_product_view():
    current_url = "/admin/product"
    return render_template("admin/product/add.html", url=current_url)


@app.route("/admin/product/add", methods=["POST"])
def add_product():
    current_url = "/admin/product"
    id = str(uuid.uuid4())
    name = request.form.get("name")
    cost = request.form.get("cost")
    price = request.form.get("price")
    qty = request.form.get("qty")
    status = 1
    img=request.form.get("img")
    if (name == "" or cost == "" or price == "" or qty == ""):
        return render_template("admin/product/add.html", url=current_url, success=False)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO product (id,name, quantity,cost,price,image,status) VALUES (?,?,?,?,?,?,?)",
                   (id, name, qty, cost, price, img, status))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return redirect(f"/admin/product?success={TRUE}&type={CREATE}")
    else:
        return redirect(f"/admin/product?success={FALSE}&type={CREATE}")


@app.route("/admin/product", methods=["POST"])
def delete_product():
    id = request.form.get("id")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM product WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(cursor.rowcount)
    if cursor.rowcount > 0:
        return redirect(f"/admin/product?success={TRUE}&type={DELETE}")
    else:
        return redirect(f"/admin/product?success={FALSE}&type={DELETE}")


@app.route("/admin/product/edit/<id>")
def edit_product_view(id):
    url = "/admin/product"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("select * from product WHERE id = ?", (id,))
    product = cursor.fetchone()
    return render_template("admin/product/edit.html", product=product, id=id, url=url)


@app.route('/api/product', methods=["PUT"])
def edit_product():
    print(request.get_json())
    query = '''
    UPDATE product 
    SET name = ?,
        cost = ?,
        price = ?,
        quantity = ?,
        status = ?,
        image = ?
    WHERE id = ?
    '''
    name = request.form.get("name")
    cost = request.form.get("cost")
    price = request.form.get("price")
    qty = request.form.get("qty")
    status = 0
    if (request.form.get("status")):
        status = 1
    img = request.form.get("img")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # cursor.execute(query, (name, cost, price, qty,
    #                        status, img, request.form.get('id')))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return redirect(f"/admin/product?success={TRUE}&type={UPDATE}")
    else:
        return redirect(f"/admin/product?success={FALSE}&type={UPDATE}")

# @app.route('/api/products')  # type: ignore
# def products():
#     try:
#         products = []
#         sql = 'SELECT p.*, c.name as category FROM product as p inner join category as c on c.id = p.cid'
#
#         search = request.args.get('search')
#         category_search = request.args.get('category')
#         if search:
#             sql = f"SELECT p.*, c.name as category FROM product as p inner join category as c on c.id = p.cid where p.name like '%{search}%'"
#         if category_search:
#             sql = f"SELECT p.*, c.name as category FROM product as p inner join category as c on c.id = p.cid where c.id = {category_search}"
#
#         result = conn.execute(text(sql))
#         conn.commit()
#
#         for row in result:
#             products.append({
#                 "id": row[0],
#                 "name": row[1],
#                 "quantity": row[2],
#                 "cost": row[3],
#                 "price": row[4],
#                 "picture": row[5],
#                 "category": row[7],
#             })
#         return products
#     except:
#         print("error")
#
#
# @app.route('/get_all_product')  # type: ignore
# def getAllProduct():
#     try:
#         category = conn.execute(text("""SELECT * FROM category """))
#
#         result = conn.execute(text(
#             """
#             SELECT
#                 product.*,
#                 category.name as 'category'
#             FROM product
#             join category on product.cid = category.id
#             """
#         ))
#         conn.commit()
#         product_arr = []
#         for item in result:
#             product_arr.append(
#                 {
#                     'id': item.id,
#                     'name': item.name,
#                     'category_id': item.cid,
#                     'cost': item.cost,
#                     'price': item.price,
#                     'category': item.category,
#                 }
#             )
#
#         category_arr = []
#         for item_cat in category:
#             category_arr.append(
#                 {
#                     'id': item_cat.id,
#                     'name': item_cat.name,
#                 }
#             )
#         data = {
#             'product': product_arr,
#             'category': category_arr
#         }
#         conn.close()
#         return data
#     except:
#         print("Error")
#
#
# @app.route('/get_product_by_category', methods=['POST'])  # type: ignore
# def getProductByCategory():
#     try:
#         if request.method == "POST":
#             category_id = request.json['category_id']
#             if category_id == 'all':
#                 result = conn.execute(text(
#                     f"""
#                     SELECT
#                         product.*,
#                         category.name as 'category'
#                     FROM product
#                     join category on product.cid = category.id
#                     """
#                 ))
#                 conn.commit()
#             else:
#                 # result = connection.execute(text(f"SELECT * FROM product where category_id = '{category_id}'"))
#                 result = conn.execute(text(
#                     f"""
#                     SELECT
#                         product.*,
#                         category.name as 'category'
#                     FROM product
#                     join category on product.cid = category.id
#                     where product.cid = '{category_id}'
#                     """
#                 ))
#                 conn.commit()
#
#             product_arr = []
#             for item in result:
#                 product_arr.append(
#                     {
#                         'id': item.id,
#                         'name': item.name,
#                         'category_id': item.cid,
#                         'category': item.category,
#                         'cost': item.cost,
#                         'price': item.price,
#                     }
#                 )
#             conn.close()
#             return product_arr
#     except:
#         print("Error")
#         return ""
