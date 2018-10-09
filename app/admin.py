import psycopg2
from flask import Blueprint
from flask import render_template
from flask import request

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/', methods=['GET', 'POST'])
def view_adminHome():

    return render_template('admin.tpl')


@admin_blueprint.route('/accounts', methods=['GET', 'POST'])
def view_accounts():

    view_table = 'Account'
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
            f" where table_name='{view_table.lower()}'",
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
        'viewaccounts.tpl', table_name=view_table, headings=headings,
        results=results,
    )


@admin_blueprint.route('/ads', methods=['GET', 'POST'])
def view_ads():

    view_table = 'advertisement'
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
            f" where table_name='{view_table.lower()}'",
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
        'viewadverts.tpl', table_name=view_table, headings=headings,
        results=results,
    )


@admin_blueprint.route('/bids', methods=['GET', 'POST'])
def view_bids():

    view_table = 'bid'
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
            f" where table_name='{view_table.lower()}'",
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
        'viewbids.tpl', table_name=view_table, headings=headings,
        results=results,
    )


@admin_blueprint.route('/rides', methods=['GET', 'POST'])
def view_rides():

    view_table = 'ride'
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
            f" where table_name='{view_table.lower()}'",
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
        'viewrides.tpl', table_name=view_table, headings=headings,
        results=results,
    )
