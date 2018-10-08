from flask import Blueprint
from flask import render_template
from flask import request
from model import Car
from model import Driver


driver_blueprint = Blueprint(
    'driver', __name__, template_folder='templates',
)


@driver_blueprint.route('/create', methods=['GET', 'POST'])
def register_driver():
    if request.method != 'POST':
        return render_template('driver.tpl')

    new_driver = Driver(**request.form)
    new_car = Car(**request.form)
    is_success = False
    try:
        print(new_driver)
        print(new_car)
        is_driver_register = new_driver.save()
        is_car_register = new_car.save()
        print(is_driver_register)
        print(is_car_register)
        is_success = is_driver_register and is_car_register

    except Exception as e:
        print(e)

    return render_template('driver.tpl', is_view=True, is_success=is_success)


@driver_blueprint.route('/', methods=['GET'])
def view_driver_registration():
    # Placeholder for profile
    return render_template('driver.tpl', is_view=False)
