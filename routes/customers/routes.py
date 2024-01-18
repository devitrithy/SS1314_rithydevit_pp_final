import sqlite3

import uuid
from flask import render_template, request, redirect
from dotenv import load_dotenv
import os
from routes.customers import customer_bp

load_dotenv()

TRUE = os.environ.get('true_code')
FALSE = os.environ.get('false_code')
CREATE = os.environ.get('create_code')
UPDATE = os.environ.get('update_code')
DELETE = os.environ.get('delete_code')

app = customer_bp


@app.route("/admin/customer")
def customer():
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
    cur.execute("SELECT * from customer;")
    customers = cur.fetchall()
    current_url = "/admin/customer"
    return render_template("admin/customer/index.html", url=current_url, customers=customers, success=succeeded,
                           type=type_name)


@app.route("/admin/customer/add")
def add_customer_view():
    current_url = "/admin/customer"
    return render_template("admin/customer/add.html", url=current_url)


@app.route("/admin/customer/add", methods=["POST"])
def add_customer():
    id = str(uuid.uuid4())
    name = request.form.get("name")
    profile_url = request.form.get("profile_url")
    status = 0
    if request.form.get("status"):
        status = 1

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customer (id,name,image,status) VALUES (?,?,?,?)",(id, name, profile_url, status))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return redirect(f"/admin/customer?success={TRUE}&type={CREATE}")
    else:
        return redirect(f"/admin/customer?success={FALSE}&type={CREATE}")


@app.route("/admin/customer", methods=["POST"])
def delete_customer():
    id = request.form.get("id")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customer WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(cursor.rowcount)
    if cursor.rowcount > 0:
        return redirect(f"/admin/customer?success={TRUE}&type={DELETE}")
    else:
        return redirect(f"/admin/customer?success={FALSE}&type={DELETE}")


@app.route("/admin/customer/edit/<id>")
def edit_customer_view(id):
    url = "/admin/customer"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("select * from customer WHERE id = ?", (id,))
    customer = cursor.fetchone()
    return render_template("admin/customer/edit.html", customer=customer, id=id, url=url)


@app.route('/admin/customer/edit', methods=["POST"])
def edit_customer():
    query = '''
    UPDATE customer 
    SET name = ?,
        image = ?,
        status = ?
    WHERE id = ?
    '''
    name = request.form.get("name")
    status = 0
    image = request.form.get("profile_url")
    if (request.form.get("status")):
        status = 1
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, (name, image, status, request.form.get('id')))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return redirect(f"/admin/customer?success={TRUE}&type={UPDATE}")
    else:
        return redirect(f"/admin/customer?success={FALSE}&type={UPDATE}")
