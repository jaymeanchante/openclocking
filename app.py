from flask import Flask
from flasgger import Swagger
from model.sqlite import init_db
from resources.routes import (
    index,
    workday,
    api_workday,
    client_workday
    )
from utils.utils import _shiftdays

app = Flask(__name__)
swagger = Swagger(app)
app.add_url_rule("/", view_func=index, methods=["GET"])
app.add_url_rule(rule="/<date>", view_func=workday, methods=["GET"])
app.add_url_rule(rule="/api/<date>", view_func=api_workday, methods=["GET", "POST", "PUT", "DELETE"])
app.add_url_rule(rule="/client/api/<date>", view_func=client_workday, methods=["GET", "POST"])
app.add_url_rule(rule="/client/api/delete/<date>", view_func=client_workday, methods=["POST"])
app.add_url_rule(rule="/client/api/put/<date>", view_func=client_workday, methods=["POST"])

app.add_template_filter(_shiftdays, "shiftdays")

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
