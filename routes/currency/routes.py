import sqlite3

import uuid
from flask import render_template, request, redirect
from dotenv import load_dotenv
import os
from routes.currency import currency_bp

load_dotenv()

TRUE = os.environ.get('true_code')
FALSE = os.environ.get('false_code')
CREATE = os.environ.get('create_code')
UPDATE = os.environ.get('update_code')
DELETE = os.environ.get('delete_code')

app = currency_bp


@app.route("/admin/currency")
def currency():
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
    cur.execute("SELECT * from currency;")
    currencys = cur.fetchall()
    current_url = "/admin/currency"
    return render_template("admin/currency/index.html", url=current_url, currencys=currencys, success=succeeded,
                           type=type_name)


@app.route("/admin/currency/add")
def add_currency_view():
    current_url = "/admin/currency"
    return render_template("admin/currency/add.html", url=current_url)


@app.route("/admin/currency/add", methods=["POST"])
def add_currency():
    id = str(uuid.uuid4())
    name = request.form.get("name")
    code = request.form.get("code")
    symbol = request.form.get("symbol")
    sell_out_price = request.form.get("sell_out_price")
    is_default = 0
    if request.form.get("is_default"):
        is_default = 1

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO currency (id,name, code,symbol,sell_out_price, is_default) VALUES (?,?,?,?,?,?)",(id, name, code, symbol, sell_out_price, is_default))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return redirect(f"/admin/currency?success={TRUE}&type={CREATE}")
    else:
        return redirect(f"/admin/currency?success={FALSE}&type={CREATE}")


@app.route("/admin/currency", methods=["POST"])
def delete_currency():
    id = request.form.get("id")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM currency WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(cursor.rowcount)
    if cursor.rowcount > 0:
        return redirect(f"/admin/currency?success={TRUE}&type={DELETE}")
    else:
        return redirect(f"/admin/currency?success={FALSE}&type={DELETE}")


@app.route("/admin/currency/edit/<id>")
def edit_currency_view(id):
    current_url = "/admin/currency"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("select * from currency WHERE id = ?", (id,))
    currency = cursor.fetchone()
    return render_template("admin/currency/edit.html", currency=currency, id=id, url=current_url)


@app.route('/admin/currency/edit', methods=["POST"])
def edit_currency():
    query = '''
    UPDATE currency 
    SET name = ?,
        code = ?,
        symbol = ?,
        sell_out_price = ?,
        is_default = ?
    WHERE id = ?
    '''
    name = request.form.get("name")
    code = request.form.get("code")
    sell_out_price = request.form.get("sell_out_price")
    symbol = request.form.get("symbol")
    is_default = 0
    if request.form.get("is_default"):
        is_default = 1
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, (name, code, symbol, sell_out_price, is_default, request.form.get('id')))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return redirect(f"/admin/currency?success={TRUE}&type={UPDATE}")
    else:
        return redirect(f"/admin/currency?success={FALSE}&type={UPDATE}")
