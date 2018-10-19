from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from model import Advertisement
from model import Driver


advertisement_blueprint = Blueprint(
    'advertisement', __name__, template_folder='templates',
)


@advertisement_blueprint.route('/view/all', methods=['GET', 'POST'])
@login_required
def view_advertisements():
    results = Advertisement.get_all()

    return render_template(
        'view_advertisement.tpl', results=results,
    )


@advertisement_blueprint.route('/view/mine', methods=['GET', 'POST'])
@login_required
def view_my_advertisements():
    driver = Driver.get_driver(current_user.get_id())
    if(driver is None):
        return redirect(url_for('driver.view_driver_registration'))

    license_number = driver[0]

    results = Advertisement.get_mine(license_number)

    return render_template('view_advertisement.tpl', results=results)


@advertisement_blueprint.route('/view/bid', methods=['GET', 'POST'])
@login_required
def bid():
    if request.method != 'POST':
        results = Advertisement.get_all()
        return render_template('view_advertisement.tpl', results=results)

    advert_start = request.form['advert_start_timestamp']
    advert_license = request.form['advert_license_number']

    advert = Advertisement.get_advert(advert_start, advert_license)

    return render_template(
        'advertisement.tpl', is_view=True,
        is_success=True, advert=advert, is_alert=False,
    )


@advertisement_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_advertisement():
    if request.method != 'POST':
        return render_template('advertisement.tpl')

    driver = Driver.get_driver(current_user.get_id())
    if(driver is None):
        return redirect(url_for('driver.view_driver_registration'))
    license_number = driver[0]

    new_advertisement = Advertisement(license_number, **request.form)
    is_success = new_advertisement.save()

    return render_template(
        'advertisement.tpl', is_view=True, is_success=is_success,
        advert=new_advertisement, is_alert=True,
    )


@advertisement_blueprint.route('/', methods=['GET'])
@login_required
def view_advertisement_creation():
    driver = Driver.get_driver(current_user.get_id())
    if(driver is None):
        return redirect(url_for('driver.view_driver_registration'))
    return render_template('advertisement.tpl', is_view=False)
