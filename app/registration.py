from logging import getLogger

from flask import Blueprint
from flask import render_template
from flask import request
from model import Account

logger = getLogger(__name__)

registration_blueprint = Blueprint(
    'registration', __name__, template_folder='templates',
)


@registration_blueprint.route('/create', methods=['GET', 'POST'])
def register_account():
    if request.method != 'POST':
        return render_template('registration.tpl')

    try:
        new_account = Account.init_using_form(**request.form)
        new_account.save()
    except TypeError as e:
        logger.error(e)
        # TODO(Nik): handle failed account creation

    return render_template('login.tpl')


@registration_blueprint.route('/', methods=['GET'])
def view_registration():
    return render_template('registration.tpl')
