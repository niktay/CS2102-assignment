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
        return render_template(
            'driver.tpl', is_view=False,
            title='Driver Registration',
        )

    new_driver = Driver(current_user.get_id(), **request.form)
    new_car = Car(**request.form)

    try:
        new_driver.save()
        new_car.save()

        print(new_driver)
        print(new_car)

    except Exception as e:
        print(e)

    return redirect(url_for('driver.get_profile'))


@driver_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def get_profile():
    driver = Driver.get_driver(current_user.get_id())
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

    update_driver = Driver(**request.form)
    update_car = Car(**request.form)

    driver = update_driver.get()
    car = update_car.get()
    is_success = False

    try:

        is_car_updated = update_car.update()
        is_driver_updated = update_driver.update()

        is_success = is_car_updated and is_driver_updated

    except Exception as e:
        print(e)

    return render_template(
        'driver.tpl', is_view=True, is_success=is_success,
        title='Profile', driver=driver, car=car,
    )


@driver_blueprint.route('/', methods=['GET'])
@login_required
def view_driver_registration():
    return render_template(
        'driver.tpl', is_view=False,
        title='Driver Registration',
    )
