from flask import Flask
from flask_assets import Environment, Bundle
from sqlite3 import connect, OperationalError
from random import randint
from argparse import ArgumentParser, Namespace
from jinja2 import Template
from json import dumps

conn = connect('mood.db', isolation_level=None)
cursor = conn.cursor()

try:
    cursor.execute('SELECT * FROM mood')
except OperationalError:
    cursor.execute('CREATE TABLE mood (user_id INTEGER, datetime DATETIME, event VARCHAR(3), satisfaction INTEGER)')

app = Flask(__name__)
assets = Environment(app)
#img_asset = Bundle()

@app.route("/")
def home():
    with open('home.html') as fh:
        return fh.read()

@app.route("/plot")
def plot():
    data = list(cursor.execute('SELECT datetime, satisfaction FROM mood WHERE user_id = 1'))
    time_data, satisfaction_data = zip(*data)

    with open('plot.html') as fh:
        return Template(fh.read()).render(
            time_data=list(map(str, time_data)),
            satisfaction_data=satisfaction_data,
            json=dumps,
        )

def

USER_IDS = {
	'Chris': 1,
}

def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('--purge', action='store_true')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    if args.purge:
        cursor.execute('DELETE FROM mood')
    else:
        for user in [(USER_IDS['Chris'], randint(0, 50) + 50, 'in'), (USER_IDS['Chris'], randint(0, 50), 'out')]:
            cursor.execute(
                'INSERT INTO mood (user_id, datetime, satisfaction, event) VALUES (?, DATETIME("now"), ?, ?)',
                user,
            )

        print(list(cursor.execute('SELECT * FROM mood')))
