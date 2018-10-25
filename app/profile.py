from logging import getLogger

from flask import Blueprint
from flask import render_template
from flask_login import current_user
from flask_login import login_required
from model import Account


logger = getLogger(__name__)

profile_blueprint = Blueprint('profile', __name__, template_folder='templates')


@profile_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def view_profile():
    account = Account.load(current_user.get_id())

    if account:
        return render_template('profile.tpl', account=account)

    logger.warning('Failed to load current user')
    logger.debug(current_user.get_id())

    return render_template('login.tpl')
