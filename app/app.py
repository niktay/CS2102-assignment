from flask import Flask
from flask import render_template
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
def landing_page():
    return render_template('login.tpl')


def run():
    app.run(debug=True, host='0.0.0.0', port=5000)
