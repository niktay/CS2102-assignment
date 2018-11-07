from logging import getLogger

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from model import Advertisement
from model import Bid
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

    advertisements = filter(lambda advert: advert.active, advertisements,)

    advertisement_data = {}
    for advertisement in advertisements:
        highest_bid = Bid.get_highest(advertisement=advertisement)

        if highest_bid is None:
            highest_bid = Bid(price=0)

        advertisement_data[advertisement] = highest_bid

    logger.debug(advertisement_data)

    return render_template(
        'view_advertisement.tpl',
        advertisements=advertisement_data, driver=driver,
    )


@advertisement_blueprint.route('/view/self', methods=['GET', 'POST'])
@login_required
def view_own_advertisements():
    driver = Driver.load(username=current_user.get_id())

    if driver is None:
        return redirect(url_for('driver.view_driver_registration'))

    advertisements = Advertisement.fetch(license_number=driver.license_number)
    highest_bid = Bid.get_highest

    return render_template(
        'advertise_rides.tpl',
        advertisements=advertisements, driver=driver, highest_bid=highest_bid,
    )


@advertisement_blueprint.route('/view/bid', methods=['GET', 'POST'])
@login_required
def bid():
    driver = Driver.load(username=current_user.get_id())

    if request.method != 'POST':
        return redirect(url_for('advertisement.view_advertisements'))

    advertisement = Advertisement.init_using_form(**request.form)

    return render_template(
        'make_bid.tpl', advertisement=advertisement, driver=driver,
    )


@advertisement_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_advertisement():
    driver = Driver.load(username=current_user.get_id())

    if request.method != 'POST':
        return render_template('advertisement.tpl', driver=driver)

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

    return render_template(
        'advertisement.tpl', is_view=False,
        driver=driver,
    )


@advertisement_blueprint.route('/close', methods=['GET', 'POST'])
@login_required
def end_bidding():
    if request.method != 'POST':
        return redirect(request.referrer)

    license_number = request.form.get('license-number', None)
    start_timestamp = request.form.get('start-timestamp', None)
    advertisement = Advertisement.fetch(
        license_number=license_number,
        start_timestamp=start_timestamp,
    )[0]

    advertisement.close_bidding()

    return redirect(request.referrer)
