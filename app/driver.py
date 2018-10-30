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

    new_driver = Driver.init_using_form(**request.form)
    new_driver.username = current_user.get_id()
    new_car = Car.init_using_form(**request.form)

    # todo(Nik): Handle case when driver is created but car fails to create
    #            try-except and do rollback
    if(new_driver.save() and new_car.save()):
        return redirect(url_for('profile.view_profile'))
    else:
        return render_template(
            'driver.tpl', is_view=True, is_success=False,
            title='Driver Registration',
        )


@driver_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def get_profile():
    driver = Driver.load(username=current_user.get_id())

    if driver is None:
        return redirect(url_for('driver.view_driver_registration'))

    car = Car.load(license_number=driver.license_number)

    return render_template(
        'driver.tpl', is_view=True, title='Your Driver Profile',
        is_success=True, driver=driver, car=car,
    )


@driver_blueprint.route('/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method != 'POST':
        return render_template('driver.tpl', is_view=False, title='Profile')

    driver = Driver.init_using_form(**request.form)
    driver.username = current_user.get_id()

    car = Car.init_using_form(**request.form)

    car.update()
    driver.update_bio()

    return redirect(url_for('driver.get_profile'))


@driver_blueprint.route('/', methods=['GET'])
@login_required
def view_driver_registration():
    driver = Driver.load(username=current_user.get_id())

    if driver:
        return redirect(url_for('driver.get_profile'))

    return render_template(
        'driver.tpl', is_view=False,
        title='Driver Registration',
    )
