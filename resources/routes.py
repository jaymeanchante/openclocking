from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for
)
from model.sqlite import (
    query_db,
    insert_db
)
from utils.utils import _get_today

def index():
    return redirect(url_for("workday", date=_get_today()))

def workday(date):
    values = query_db("SELECT * FROM dates WHERE date=?", (date,))
    return render_template("index.html", values=values)

def api_workday(date):
    """Clocked times endpoint
    Route to interact with clocked times in a given date.
    ---
    responses:
      200:
        description: A list of clocked times
        examples:
          '2020-12-23'
    tags:
      - Clocked dates
    get:
      parameters:
        - name: date
          in: path
          type: string
          required: true
    post:
      parameters:
        - name: date
          in: path
          type: string
          required: true
        - name: time
          in: formData
          type: string
          required: true
    put:
      parameters:
        - name: date
          in: path
          type: string
          required: true
        - name: id
          in: formData
          type: integer
          required: true
        - name: time
          in: formData
          type: string
          required: true
    delete:
      parameters:
        - name: date
          in: path
          type: string
          required: true
        - name: id
          in: formData
          type: integer
          required: true
    """
    values = query_db("SELECT * FROM dates WHERE date=?", (date,))
    idx = len(values)
    if request.method == "GET":
        return jsonify(values)
    elif request.method == "POST":
        time = request.form["time"]
        insert_db("INSERT INTO dates (date, idx, time) VALUES (?, ?, ?)", (date, idx, time))
        return jsonify(query_db("SELECT * FROM dates WHERE date=?", (date,)))
    elif request.method == "DELETE":
        id = request.form["id"]
        insert_db("DELETE FROM dates WHERE id=?", (id,))
        return jsonify(query_db("SELECT * FROM dates WHERE date=?", (date,)))
    elif request.method == "PUT":
        id = request.form["id"]
        time = request.form["time"]
        insert_db("UPDATE dates SET time=? WHERE id=?", (time,id,))
        return jsonify(query_db("SELECT * FROM dates WHERE date=?", (date,)))

def client_workday(date):
    values = query_db("SELECT * FROM dates WHERE date=?", (date,))
    idx = len(values)
    if request.method == "POST" and "delete" in request.path:
        id = request.form["id"]
        insert_db("DELETE FROM dates WHERE id=?", (id,))
        return redirect(url_for("workday", date=date))
    elif request.method == "POST" and "put" in request.path:
        id = request.form["id"]
        time = request.form["time"]
        insert_db("UPDATE dates SET time=? WHERE id=?", (time,id,))
        return redirect(url_for("workday", date=date))
    elif request.method == "POST":
        time = request.form["time"]
        insert_db("INSERT INTO dates (date, idx, time) VALUES (?, ?, ?)", (date, idx, time))
        return redirect(url_for("workday", date=date))