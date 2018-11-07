from collections import namedtuple

from flask import Blueprint
from flask import render_template
from flask_login import current_user
from flask_login import login_required
from model import Advertisement
from model import Driver
from model import Ride

ride_blueprint = Blueprint('ride', __name__, template_folder='templates',)


@ride_blueprint.route('/view/upcoming', methods=['GET', 'POST'])
@login_required
def view_upcoming():
    username = current_user.get_id()
    bids_for_upcoming_rides = Ride.fetch(username=username, upcoming=True)

    won_advertisement = {}
    Details = namedtuple('Details', 'car bid')
    for bid in bids_for_upcoming_rides:
        advertisement = Advertisement.fetch(
            license_number=bid.license_number,
            start_timestamp=bid.start_timestamp,
        )[0]
        won_advertisement[advertisement] = Details(
            car=advertisement.car(),
            bid=bid,
        )

    driver = Driver.load(username=username)

    return render_template(
        'scheduled_rides.tpl', upcoming=won_advertisement,
        driver=driver,
    )


@ride_blueprint.route('/view/past', methods=['GET', 'POST'])
@login_required
def view_history():
    username = current_user.get_id()
    bids_for_upcoming_rides = Ride.fetch(username=username, past=True)

    won_advertisement = {}
    Details = namedtuple('Details', 'car bid')
    for bid in bids_for_upcoming_rides:
        advertisement = Advertisement.fetch(
            license_number=bid.license_number,
            start_timestamp=bid.start_timestamp,
        )[0]
        won_advertisement[advertisement] = Details(
            car=advertisement.car(),
            bid=bid,
        )

    driver = Driver.load(username=username)

    return render_template(
        'past_rides.tpl', past=won_advertisement,
        driver=driver,
    )
