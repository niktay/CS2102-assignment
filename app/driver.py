from flask import Blueprint
from flask import render_template
from flask import request
from model import Driver


driver_blueprint = Blueprint(
    'driver', __name__, template_folder='templates',
)


@driver_blueprint.route('/create', methods=['GET', 'POST'])
def register_driver():
    if request.method != 'POST':
        return render_template('driver.tpl')

    new_driver = Driver(**request.form)
    is_success = 0
    try:
        print(new_driver)
        is_success = new_driver.save()
    except Exception as e:
        print(e)

    return render_template('driver.tpl', is_view = 0, is_success=is_success)


@driver_blueprint.route('/', methods=['GET'])
def view_driver_registration():
    # Placeholder for profile
    return render_template('driver.tpl', is_view = 1)
