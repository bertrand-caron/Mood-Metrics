from flask import Flask, request
from flask_assets import Environment, Bundle
from sqlite3 import connect, OperationalError
from random import randint
from argparse import ArgumentParser, Namespace
from jinja2 import Template
from json import dumps, loads
from os.path import basename, join
from ast import literal_eval

from facial import satisfaction_score_for

conn = connect('mood.db', isolation_level=None)
cursor = conn.cursor()

try:
    cursor.execute('SELECT * FROM mood')
except OperationalError:
    cursor.execute('CREATE TABLE mood (user_id INTEGER, datetime DATETIME, event VARCHAR(3), satisfaction INTEGER, image_url VARCHAR(1000))')

ASSETS_DIR = 'assets'

app = Flask(__name__)
assets = Environment(app)
#img_asset = Bundle()

@app.route("/")
def home():
    with open('home.html') as fh:
        return fh.read()

@app.route("/plot")
def plot():
    user_id = 447893
    data = list(cursor.execute('SELECT datetime, satisfaction FROM mood WHERE user_id = ? ORDER BY DATETIME(datetime) ASC', (user_id,)))
    print(data)
    if len(data) > 0:
        time_data, satisfaction_data = zip(*data)
    else:
        time_data, satisfaction_data = [], []

    daily_average = list(cursor.execute('SELECT AVG(satisfaction) FROM mood WHERE user_id = ? AND DATETIME(datetime) >= DATETIME("now", "-1 days")', (user_id,)))[0][0]
    all_time_average = list(cursor.execute('SELECT AVG(satisfaction) FROM mood WHERE user_id = ?', (user_id,)))[0][0]

    with open('plot.html') as fh:
        return Template(fh.read()).render(
            time_data=list(map(str, time_data)),
            satisfaction_data=satisfaction_data,
            daily_average=daily_average,
            all_time_average=all_time_average,
            json=dumps,
        )

@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    try:
        json_payload = loads(request.data.decode())['payload']
        user_id, photo_url = map(lambda key: json_payload['body'][key], ['user_id', 'photo'])

        photo_url, *_ = photo_url.split('?')
        score = satisfaction_score_for(photo_url)
        cursor.execute(
            'INSERT INTO mood (user_id, datetime, satisfaction, event, image_url) VALUES (?, DATETIME("now"), ?, "in", ?)',
            (user_id, score, photo_url),
        )
        return 'Success'
    except:
        raise

USER_IDS = {
	'Chris': 1,
}

def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('--purge', action='store_true')
    parser.add_argument('--import-data', type=str, default=None)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    if args.purge:
        cursor.execute('DELETE FROM mood')
    elif args.import_data is not None:
        with open(args.import_data) as fh:
            data = literal_eval(fh.read())
        print(data)
        assert isinstance(data, list) and all(len(row) == 5 for row in data), data
        cursor.executemany(
            'INSERT INTO mood (user_id, datetime, satisfaction, event, image_url) VALUES (?, ?, ?, ?, ?)',
            data,
        )
    else:
        print(list(cursor.execute('SELECT * FROM mood')))
