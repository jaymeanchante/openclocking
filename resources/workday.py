from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for
)

workdays = {}

def _create_if_not_exist(date):
    if date not in workdays.keys():
        workdays[date] = []
    pass

def workday(date):
    _create_if_not_exist(date)
    values = workdays[request.path.split("/")[-1]]
    if "api" in request.path:
        if request.method == "GET":
            return jsonify(workdays[date])
        elif request.method == "POST":
            workdays[date].append(request.form["time"])
            if "client" in request.path:
                return redirect(url_for("workday", date=date))
            return jsonify({date: workdays[date]})
    return render_template("index.html", date=date, values=values)
