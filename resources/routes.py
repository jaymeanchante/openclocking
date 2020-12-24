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
    if request.method == "GET":
        return jsonify(values)
    elif request.method == "POST":
        time = request.form["time"]
        insert_db("INSERT INTO dates (date, time) VALUES (?, ?)", (date, time))
        return jsonify(query_db("SELECT * FROM dates WHERE date=?", (date,)))
    elif request.method == "DELETE":
        time = request.form["time"]
        insert_db("DELETE FROM dates WHERE date=? AND time=?", (date, time))
        return jsonify(query_db("SELECT * FROM dates WHERE date=?", (date,)))
    elif request.method == "PUT":
        old_time = request.form["old_time"]
        new_time = request.form["new_time"]
        insert_db("UPDATE dates SET time=? WHERE date=? AND time=?", (new_time, date, old_time))
        return jsonify(query_db("SELECT * FROM dates WHERE date=?", (date,)))

def client_workday(date):
    values = query_db("SELECT * FROM dates WHERE date=?", (date,))
    if request.method == "POST" and "delete" in request.path:
        time = request.form["time"]
        insert_db("DELETE FROM dates WHERE date=? AND time=?", (date, time))
        return redirect(url_for("workday", date=date))
    elif request.method == "POST" and "put" in request.path:
        old_time = request.form["old_time"]
        new_time = request.form["new_time"]
        insert_db("UPDATE dates SET time=? WHERE date=? AND time=?", (new_time, date, old_time))
        return redirect(url_for("workday", date=date))
    elif request.method == "POST":
        time = request.form["time"]
        insert_db("INSERT INTO dates (date, time) VALUES (?, ?)", (date, time))
        return redirect(url_for("workday", date=date))

def import_data():
    if request.method == "GET":
        return render_template("import.html")
    elif request.method == "POST":
        file = request.files["file"]
        lines = file.stream.readlines()
        success = "unsuccessful"
        values = {}
        try:
          for i in range(len(lines)):
              if "###PREFERENCES_END" in lines[i].decode():
                  break
          for line in lines[i+1:]:
              line_split = line.decode().split()
              date = line_split[0]
              time = line_split[1].split(";")[0]
              insert_db("INSERT INTO dates (date, time) VALUES (?, ?)", (date, time))
          values["Imported"] = f"{len(lines[i+1:])} entries"
          values["Last entry"] = f"was date {date} at time {time}"
          success = "successful"
        except:
          pass
        return render_template("transition_after_import.html", success=success, values=values)