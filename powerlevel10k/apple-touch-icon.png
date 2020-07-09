from flask import Blueprint, render_template, request, redirect, url_for, Response

from . import db
from . import auth

bp = Blueprint("todos", __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    """As a user, I want to see a list of my to-do items to know what to work on."""

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)


@bp.route('/add', methods=('GET', 'POST'))
def add():
    """As a user, I want to submit a form to add new items to my list."""
    if request.method == 'POST':
        with db.get_db() as con:
            with con.cursor() as cur:
                add = request.form['add']
                cur.execute("""INSERT INTO todos (description, completed, created_at)
                VALUES (%s, %s, NOW())
                """,
                            (add, False)
                            )

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)


@bp.route('/profile', methods=('GET', 'POST'))
def profile():
    return render_template("profile.html")

#######################################################################################
#Each request to the RESTful system commonly uses these 4 HTTP verbs:
#GET: Get a specific resource or a collection of resources
#POST: Create a new resource
#PUT: Update a specific resource
#DELETE: Remove a specific resource
#Although others are permitted and sometimes used, like PATCH, HEAD, and OPTIONS.3
########################################################################################
