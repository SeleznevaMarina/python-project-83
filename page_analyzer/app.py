from flask import Flask, render_template, redirect, request
import psycopg2
import os
import urllib

app = Flask(__name__)


DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect("dbname=analyzer user=saselezn")


# def get_query(file):

#     with open(file, "r") as f:
#         return f.read()


def execute_query(connection, query):
    # connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except psycopg2.Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except psycopg2.Error as e:
        print(f"The error '{e}' occurred")


@app.post('/urls')
def add_url():
    url = request.form.get('url')
    # url_record = urllib.parse.urlparse(url)
    insert_query = (
        f"INSERT INTO urls (name) VALUES (\'{url}\');"
        )

    conn.autocommit = True
    select_query = (
        f"SELECT id FROM urls WHERE name = \'{url}\';"
        )
    id = execute_read_query(conn, select_query)
    print ('id=', id)

    return redirect(f'/urls/{id}')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls/<id>')
def get_url(id):
    select_query = (
        f"SELECT * FROM urls WHERE id = {id};"
        )
    url_record = execute_query(conn, select_query)
    # print(url_record)
    return render_template('urls/show.html', url=url_record)


@app.route('/urls')
def get_urls():
    select_query = (
        f"SELECT * FROM urls;"
        )
    url_records = execute_query(conn, select_query)

    if url_records is None:
        url_records = []

    return render_template('urls/index.html', urls=url_records)
