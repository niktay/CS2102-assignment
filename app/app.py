import psycopg2
from flask import Flask

app = Flask(__name__)


@app.route('/')
def view_records():
    try:
        # TODO(Nik): Secrets management
        conn = psycopg2.connect(
            dbname='admin', user='admin',
            password='secret', host='db',
            port='5432',
        )
    except Exception as e:
        # TODO(Nik): Error handling/logging
        print(e)

    cur = conn.cursor()
    results = []
    try:
        cur.execute('SELECT * FROM test;')
        results = cur.fetchall()
    except Exception as e:
        # TODO(Nik): Error handling/logging
        print(e)

    conn.close()
    cur.close()
    return f'Results: {results}'


def run():
    app.run(debug=True, host='0.0.0.0', port=5000)
