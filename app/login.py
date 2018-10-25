from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_user
from flask_login import logout_user
from model import Account

from app.app import login_manager


login_blueprint = Blueprint('login', __name__, template_folder='templates')


@login_blueprint.route('/', methods=['GET', 'POST'])
def view_login_form():
    return render_template('login.tpl')


@login_blueprint.route('/auth', methods=['GET', 'POST'])
def process_login():
    if request.method != 'POST':
        return render_template('login.tpl')

    account = Account.init_using_form(**request.form)

    if account.authenticate():
        login_user(account)
        return redirect(url_for('profile.view_profile'))
    else:
        return render_template('login.tpl')


@login_blueprint.route('/deauth', methods=['GET', 'POST'])
def process_logout():
    logout_user()
    return redirect(url_for('login.view_login_form'))


@login_manager.user_loader
def load_user(username):
    return Account.load(username)
