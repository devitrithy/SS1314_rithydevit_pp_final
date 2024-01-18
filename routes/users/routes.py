import sqlite3

import uuid
from flask import render_template, request, redirect
from dotenv import load_dotenv
import os
from routes.users import user_bp

load_dotenv()

TRUE = os.environ.get('true_code')
FALSE = os.environ.get('false_code')
CREATE = os.environ.get('create_code')
UPDATE = os.environ.get('update_code')
DELETE = os.environ.get('delete_code')

app = user_bp


@app.route("/admin/user")
def user():
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
    cur.execute("SELECT * from user;")
    users = cur.fetchall()
    current_url = "/admin/user"
    return render_template("admin/user/index.html", url=current_url, users=users, success=succeeded,
                           type=type_name)


@app.route("/admin/user/add")
def add_user_view():
    current_url = "/admin/user/add"
    return render_template("admin/user/add.html", url=current_url)


@app.route("/admin/user/add", methods=["POST"])
def add_user():
    id = str(uuid.uuid4())
    name = request.form.get("name")
    profile_url = request.form.get("profile_url")
    status = 0
    if request.form.get("status"):
        status = 1

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (id,name,image,status) VALUES (?,?,?,?)",(id, name, profile_url, status))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return redirect(f"/admin/user?success={TRUE}&type={CREATE}")
    else:
        return redirect(f"/admin/user?success={FALSE}&type={CREATE}")


@app.route("/admin/user", methods=["POST"])
def delete_user():
    id = request.form.get("id")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(cursor.rowcount)
    if cursor.rowcount > 0:
        return redirect(f"/admin/user?success={TRUE}&type={DELETE}")
    else:
        return redirect(f"/admin/user?success={FALSE}&type={DELETE}")


@app.route("/admin/user/edit/<id>")
def edit_user_view(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("select * from user WHERE id = ?", (id,))
    user = cursor.fetchone()
    return render_template("admin/user/edit.html", user=user, id=id)


@app.route('/admin/user/edit', methods=["POST"])
def edit_user():
    query = '''
    UPDATE user 
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
        return redirect(f"/admin/user?success={TRUE}&type={UPDATE}")
    else:
        return redirect(f"/admin/user?success={FALSE}&type={UPDATE}")
