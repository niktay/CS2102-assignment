from flask import Blueprint
from flask import render_template


driver_blueprint = Blueprint('drivers', __name__, template_folder='templates')


@driver_blueprint.route('/', methods=['GET', 'POST'])
def view_profile():
    # Placeholder for profile
    return render_template('driver.tpl')
