from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from model import Car
from model import Driver

driver_blueprint = Blueprint('driver', __name__, template_folder='templates',)


@driver_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def register_driver():
    if request.method != 'POST':
        return redirect(url_for('driver.view_driver_registration'))

    new_driver = Driver(current_user.get_id(), **request.form)
    new_car = Car(**request.form)
    is_success = False

    is_driver_created = new_driver.save()
    is_car_created = new_car.save()
    is_success = is_driver_created and is_car_created

    if(is_success):
        return redirect(url_for('driver.get_profile'))
    else:
        return render_template(
            'driver.tpl', is_view=True, is_success=False,
            title='Driver Registration',
        )


@driver_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def get_profile():
    driver = Driver.get_driver(current_user.get_id())

    if(driver is None):
        return redirect(url_for('driver.view_driver_registration'))

    license_number = driver[0]

    car = Car.get_car(license_number)

    return render_template(
        'driver.tpl', is_view=True, title='Your Driver Profile',
        is_success=True, driver=driver, car=car,
    )


@driver_blueprint.route('/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method != 'POST':
        return render_template('driver.tpl', is_view=False, title='Profile')

    update_driver = Driver(current_user.get_id(), **request.form)

    update_car = Car(**request.form)

    is_success = update_car.update()
    is_success = is_success and update_driver.update()

    return redirect(url_for('driver.get_profile'))


@driver_blueprint.route('/', methods=['GET'])
@login_required
def view_driver_registration():
    driver = Driver.get_driver(current_user.get_id())
    if(driver is not None):
        return redirect(url_for('driver.get_profile'))

    return render_template(
        'driver.tpl', is_view=False,
        title='Driver Registration',
    )
