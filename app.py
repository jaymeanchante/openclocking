from flask import Flask
from model.sqlite import init_db
from resources.workday import workday
from resources.index import index

app = Flask(__name__)
app.add_url_rule("/", view_func=index, methods=["GET"])
app.add_url_rule(rule="/<date>", view_func=workday, methods=["GET", "POST", "PUT", "DELETE"])
app.add_url_rule(rule="/api/<date>", view_func=workday, methods=["GET", "POST", "PUT", "DELETE"])
app.add_url_rule(rule="/client/api/<date>", view_func=workday, methods=["GET", "POST", "PUT", "DELETE"])

init_db()

if __name__ == "__main__":
    app.run(debug=True)
