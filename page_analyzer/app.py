from flask import Flask, render_template, redirect, request
import psycopg2
import os
import urllib

app = Flask(__name__)


DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect("dbname=analyzer user=saselezn")


def get_data(path):

    with open(path, "r") as f:
        return f.read()


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except psycopg2.Error as e:
        print(f"The error '{e}' occurred")



create_table = get_data('database.sql')
execute_query(conn, create_table)


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except psycopg2.Error as e:
        print(f"The error '{e}' occurred")


def normalize_url(url):
    url_parse = urllib.parse.urlparse(url)
    normalized_url = url_parse._replace(fragment="").geturl()
    return normalized_url


def validate_url(url):


@app.post('/urls')
def add_url():
    url = request.form.get('url')
    url = normalize_url(url)
    errors = validate(url)
    insert_query = (
        f"INSERT INTO urls (name) VALUES (\'{url}\');"
        )

    execute_query(conn, insert_query)
    select_query = (
        f"SELECT id FROM urls WHERE name = \'{url}\';"
        )
    (id,) = execute_read_query(conn, select_query)[0]

    return redirect(f'/urls/{id}')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls/<id>')
def get_url(id):
    select_query = (
        f"SELECT * FROM urls WHERE id = {id};"
        )
    (id, name, created_at) = execute_read_query(conn, select_query)[0]

    return render_template('urls/show.html',
    id=id, name=name,
    created_at=created_at)


@app.route('/urls')
def get_urls():
    select_query = (
        f"SELECT * FROM urls;"
        )
    url_records = execute_read_query(conn, select_query)

    if url_records is None:
        url_records = []

    return render_template('urls/index.html',
    urls=url_records,
    code=200)
