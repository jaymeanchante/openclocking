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

def workday(date):
    values = [i["time"] for i in query_db("SELECT time FROM dates WHERE date=?", (date,))]
    idx = len(values)
    if "api" in request.path:
        if request.method == "GET":
            return jsonify(values)
        elif request.method == "POST":
            time = request.form["time"]
            insert_db("INSERT INTO dates (date, idx, time) VALUES (?, ?, ?)", (date, idx, time))
            if "client" in request.path:
                return redirect(url_for("workday", date=date))
            return jsonify({date: [i["time"] for i in query_db("SELECT time FROM dates WHERE date=?", (date,))] })
        elif request.method == "DELETE":
            id = request.form["id"]
            insert_db("DELETE FROM dates WHERE id=?", (id,))
            return jsonify({date: [i["time"] for i in query_db("SELECT time FROM dates WHERE date=?", (date,))] })
        elif request.method == "PUT":
            id = request.form["id"]
            time = request.form["time"]
            insert_db("UPDATE dates SET time=? WHERE id=?", (time,id,))
            return jsonify({date: [i["time"] for i in query_db("SELECT time FROM dates WHERE date=?", (date,))] })
    return render_template("index.html", date=date, values=values)
