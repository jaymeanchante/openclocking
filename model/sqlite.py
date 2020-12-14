import sqlite3
from flask import g, Flask

app = Flask(__name__)

DATABASE = "database.db"

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
            for idx, value in enumerate(row))

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
            db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=(), one=False):
    db = get_db()
    try:
        cur = db.execute(query, args)
        db.commit()
    except:
        db.rollback()
    pass
