import datetime
from flask import redirect, url_for

def _get_today():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def index():
    return redirect(url_for("workday", date=_get_today()))
