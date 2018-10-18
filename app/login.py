from logging import getLogger

from flask import Blueprint
from flask import render_template
from flask import request
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from model import Account

from app.app import login_manager


login_blueprint = Blueprint('login', __name__, template_folder='templates')
logger = getLogger(__name__)


@login_blueprint.route('/', methods=['GET', 'POST'])
def view_login_form():
    return render_template('login.tpl')


@login_blueprint.route('/auth', methods=['GET', 'POST'])
def process_login():
    if request.method != 'POST':
        return render_template('login.tpl')

    account = Account.init_using_form(**request.form)

    logger.debug(account)
    logger.debug(type(account))
    logger.debug(type(account.authenticate))
    if account.authenticate():
        login_user(account)
        return f'<h1>Login Success! Welcome {current_user.get_id()}</h1>'
    else:
        return '<h1>Invalid Credentials!</h1>'


@login_blueprint.route('/deauth', methods=['GET', 'POST'])
def process_logout():
    logout_user()
    return render_template('login.tpl')


@login_manager.user_loader
def load_user(username):
    print(f'Loading user {username}')
    logger.debug(f'{Account.load}')
    logger.debug(f'{dir(Account.load)}')
    logger.debug(f'{type(Account.load)}')
    user = Account.load(username)
    return user
