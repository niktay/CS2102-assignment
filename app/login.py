from flask import Blueprint
from flask import render_template
from flask import request
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from model import Account

from app import login_manager


login_blueprint = Blueprint('login', __name__, template_folder='templates')


@login_blueprint.route('/', methods=['GET', 'POST'])
def view_login_form():
    return render_template('login.tpl')


@login_blueprint.route('/auth', methods=['GET', 'POST'])
def process_login():
    if request.method != 'POST':
        return render_template('login.tpl')

    account = Account(**request.form)

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
    return Account.load(username)
