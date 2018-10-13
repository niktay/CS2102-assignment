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


username = '1234abc'
driver = None
car = None


@driver_blueprint.route('/create', methods=['GET', 'POST'])
def register_driver():
    if request.method != 'POST':
        return render_template(
            'driver.tpl', is_view=False,
            title='Driver Registration',
        )

    new_driver = Driver(**request.form)
    new_car = Car(**request.form)

    global driver
    driver = new_driver.get()
    global car
    car = new_car.get()

    try:
        print(new_driver)
        print(new_car)
        new_driver.save()
        new_car.save()

    except Exception as e:
        print(e)

    return redirect(url_for('driver.get_profile'))


@driver_blueprint.route('/profile', methods=['GET', 'POST'])
def get_profile():
    global driver
    global car

    profile_driver = driver
    profile_car = car

    return render_template(
        'driver.tpl', is_view = True, title = 'Your Driver Profile',
        is_success = True, driver = profile_driver, car = profile_car,
    )


@driver_blueprint.route('/update', methods=['GET', 'POST'])
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
        'driver.tpl', is_view = True, is_success = is_success,
        title = 'Profile', driver = driver, car = car,
    )



@driver_blueprint.route('/', methods=['GET'])
@login_required
def view_driver_registration():
    return render_template(
        'driver.tpl', is_view = False,
        title = 'Driver Registration',
    )
