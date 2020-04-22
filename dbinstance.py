import sqlite3
from flask import Flask, request, jsonify, g, Response

# instance not exactly needed in this case as we are dealing with single database
# important in the cases when dealing with multiple databases

app = Flask(__name__)
USER_DATABASE = './reddit.db'

def get_userdb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(USER_DATABASE)  #create a database instance and use it for later execution
        print("database instance is created")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
