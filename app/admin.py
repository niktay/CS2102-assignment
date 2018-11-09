import psycopg2
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from model import Account
from model import Advertisement
from model import Bid
from model import Driver
from model import Ride

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def view_dashboard():
    account = Account.load(current_user.get_id())
    if not account.is_admin:
        return redirect(url_for('profile.view_profile'))

    return render_template(
        'admin.tpl',
        bid_count=Advertisement.total_by_month(),
        ride_count=Ride.total_by_month(),
        active_count=Account.active_count(),
        inactive_count=Account.inactive_count(),
        bid_hourly_data=Bid.dump_hourly_jinja(),
        top_drivers=Driver.get_top_drivers(),
        _enumerate=enumerate,
    )


@admin_blueprint.route('/view/<string:table_name>', methods=['GET', 'POST'])
@login_required
def view_table(table_name):
    account = Account.load(current_user.get_id())
    if not account.is_admin:
        return redirect(url_for('profile.view_profile'))

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
