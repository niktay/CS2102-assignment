import psycopg2
from flask import Blueprint
from flask import render_template

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/', methods=['GET', 'POST'])
def view_dashboard():
    return render_template('admin.tpl')


@admin_blueprint.route('/view/<string:table_name>', methods=['GET', 'POST'])
def view_table(table_name):
    try:
        # TODO(Nik): Secrets management
        conn = psycopg2.connect(
            dbname='admin', user='admin', password='secret', host='db',
            port='5432',
        )
    except Exception as e:
        # TODO(Nik): Error handling/logging
        print(e)
    cur = conn.cursor()

    headings = []
    results = []
    try:
        cur.execute(
            'select column_name from information_schema.columns'
            f" where table_name='{table_name.lower()}'",
        )
        headings = cur.fetchall()

        cur.execute(f'SELECT * FROM {table_name.lower()};')
        results = cur.fetchall()
    except Exception as e:
        # TODO(Nik): Error handling/logging
        print(e)

    conn.close()
    cur.close()
    return render_template(
        'table_view.tpl', table_name=table_name, headings=headings,
        results=results,
    )
