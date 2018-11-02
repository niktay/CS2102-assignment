from logging import getLogger

from flask import Blueprint
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from model import Bid
from model import Car

logger = getLogger(__name__)


bid_blueprint = Blueprint(
    'bid', __name__, template_folder='templates',
)


@bid_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_bid():
    if request.method != 'POST':
        return redirect(request.referrer)

    bid = Bid.init_using_form(**request.form)

    bid.username = current_user.get_id()

    license_number = Car.load(
        license_plate=request.form['license-plate'],
    ).license_number
    bid.license_number = license_number

    logger.debug(f'going to save {bid}')

    if bid.save():
        return redirect(url_for('advertisement.view_advertisements'))

    return redirect(request.referrer)
