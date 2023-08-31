import sqlite3

from flask import Flask, json, render_template, jsonify, request, url_for, redirect, flash, g
from custom_logging import logging_message
from query_db import get_post_count, get_db_connection_count


# Function to get a database connection.
# This function connects to database with the name `database.db`

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                              (post_id,)).fetchone()
    connection.close()
    return post


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route("/healthz", endpoint="healthz")
@logging_message(app)
def healthz():
    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype="application/json",
    )
    return response


# https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
@app.route("/metrics", endpoint="metrics")
@logging_message(app)
def metrics():
    post_count = get_post_count()
    db_connection_count = get_db_connection_count()

    metrics_data = {
        "db_connection_count": db_connection_count,
        "post_count": post_count
    }

    return jsonify(metrics_data), 200


# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)


# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        return render_template('404.html'), 404
    else:
        return render_template('post.html', post=post)


# Define the About Us page
@app.route('/about')
def about():
    return render_template('about.html')


# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                               (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')


@app.teardown_request
def teardown_request(exception=None):
    if hasattr(g, 'db_connection'):
        connection = getattr(g, 'db_connection')
        connection.close()
        del g.db_connection


# start the application on port 3111
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3111, debug=True)
