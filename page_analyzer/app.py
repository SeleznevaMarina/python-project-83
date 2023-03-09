from flask import Flask, render_template
# import psycopg2
import os


app = Flask(__name__)

url = {'name': 'https://ru.hexlet.io', 'id': 1,}
urls = [{'name': 'https://ru.hexlet.io', 'id': 1,}, {'name': 'https://proglib.io/', 'id': 2,}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/urls/<id>')
def get_url(id):
    return render_template('urls/show.html', url=url)


@app.route('/urls')
def get_urls():
    return render_template('urls/index.html', urls=urls)


# @app.route('/')
# def add_url():
#     DATABASE_URL = os.getenv('DATABASE_URL')
#     conn = psycopg2.connect(DATABASE_URL)
#     url_record = urllib.parse.urlparse(url)

#     insert_query = (
#         f"INSERT INTO urls (name) VALUES {url_record}"
#         )

#     conn.autocommit = True
#     cursor = connection.cursor()
#     cursor.execute(insert_query, users)

