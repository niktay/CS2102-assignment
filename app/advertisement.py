from logging import getLogger

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from model import Advertisement
from model import Driver

logger = getLogger(__name__)


advertisement_blueprint = Blueprint(
    'advertisement', __name__, template_folder='templates',
)


@advertisement_blueprint.route('/view', methods=['GET', 'POST'])
@login_required
def view_advertisements():
    driver = Driver.load(username=current_user.get_id())

    advertisements = Advertisement.fetch()

    if driver:
        advertisements = filter(
            lambda advert: advert.license_number != driver.license_number,
            advertisements,
        )

    return render_template(
        'view_advertisement.tpl',
        advertisements=advertisements,
    )


@advertisement_blueprint.route('/view/self', methods=['GET', 'POST'])
@login_required
def view_own_advertisements():
    driver = Driver.load(username=current_user.get_id())

    if driver is None:
        return redirect(url_for('driver.view_driver_registration'))

    advertisements = Advertisement.fetch(license_number=driver.license_number)

    return render_template(
        'advertise_rides.tpl',
        advertisements=advertisements,
    )


@advertisement_blueprint.route('/view/bid', methods=['GET', 'POST'])
@login_required
def bid():
    if request.method != 'POST':
        return redirect(url_for('advertisement.view_advertisements'))

    advertisement = Advertisement.init_using_form(**request.form)

    return render_template('make_bid.tpl', advertisement=advertisement)


@advertisement_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_advertisement():
    if request.method != 'POST':
        return render_template('advertisement.tpl')

    driver = Driver.load(username=current_user.get_id())

    if driver is None:
        return redirect(url_for('driver.view_driver_registration'))

    advertisement = Advertisement.init_using_form(**request.form)
    advertisement.license_number = driver.license_number
    advertisement.save()

    return redirect(url_for('advertisement.view_own_advertisements'))


@advertisement_blueprint.route('/', methods=['GET'])
@login_required
def view_advertisement_creation():
    driver = Driver.load(username=current_user.get_id())

    if driver is None:
        return redirect(url_for('driver.view_driver_registration'))

    return render_template('advertisement.tpl', is_view=False)
