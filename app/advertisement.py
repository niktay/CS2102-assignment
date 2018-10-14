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


@advertisement_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_advertisement_form():
    if request.method != 'POST':
        return render_template('advertisement.tpl')

    driver = Driver.get_driver(current_user.get_id())
    license_number = driver[0]

    new_advertisement = Advertisement(license_number, **request.form)
    is_success = False
    try:
        print(new_advertisement)
        is_success = new_advertisement.save()

    except Exception as e:
        print(e)

    return render_template(
        'advertisement.tpl', is_view=True, is_success=is_success,
    )


@advertisement_blueprint.route('/', methods=['GET'])
@login_required
def view_advertisement_creation():
    driver = Driver.get_driver(current_user.get_id())
    if(driver is None):
        return redirect(url_for('driver.view_driver_registration'))
    return render_template('advertisement.tpl', is_view=False)
