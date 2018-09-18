import psycopg2
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def view_records():
    view_table = 'Account'
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

    if request.method == 'POST':
        result = request.form
        try:
            cur.execute(result['command'])
            conn.commit()
        except Exception as e:
            print(e)

    headings = []
    results = []
    try:
        cur.execute(
            'select column_name from information_schema.columns'
            f" where table_name='{view_table}'",
        )
        headings = cur.fetchall()
        cur.execute(f'SELECT * FROM {view_table};')
        results = cur.fetchall()
    except Exception as e:
        # TODO(Nik): Error handling/logging
        print(e)

    conn.close()
    cur.close()
    return render_template(
        'dashboard.tpl', table_name=view_table,
        headings=headings, results=results,
    )


def run():
    app.run(debug=True, host='0.0.0.0', port=5000)
