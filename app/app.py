import psycopg2
from flask import Flask
from flask import render_template
from flask import request
from flask_login import current_user
from flask_login import LoginManager
from log import setup_logger

logger = setup_logger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'  # TODO(niktay): secrets management

login_manager = LoginManager()
login_manager.init_app(app)
logger.info(f'Initialized LoginManager()')

# Defer import of blueprints as they require login_manager to be defined
from admin import admin_blueprint  # noqa: E402
from adminitise import adminitise_blueprint  # noqa: E402
from driver import driver_blueprint  # noqa: E402
from registration import registration_blueprint  # noqa: E402
from advertisement import advertisement_blueprint  # noqa:E402
import login  # noqa: E402

try:
    logger.info(f'Registering blueprints')

    app.register_blueprint(driver_blueprint, url_prefix='/driver')
    app.register_blueprint(login.login_blueprint, url_prefix='/login')
    app.register_blueprint(registration_blueprint, url_prefix='/register')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(adminitise_blueprint, url_prefix='/adminitise')
    app.register_blueprint(
        advertisement_blueprint,
        url_prefix='/advertisement',
    )

    logger.info(f'Registered blueprints')
except NameError as e:
    logger.error(e)
except Exception:
    logger.exception('Failed to register blueprints')

login_manager.login_view = 'login.view_login_form'
logger.debug(f'Login view set to {login_manager.login_view}')
logger.info(f'Registered login view to LoginManager')


@app.route('/', methods=['GET', 'POST'])
def view_records():
    logger.error(current_user)
    logger.error(type(current_user))
    logger.error(dir(current_user))
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
        'dashboard.tpl', table_name=view_table, headings=headings,
        results=results,
    )


def run():
    app.run(debug=True, host='0.0.0.0', port=5000)
