from flask import Blueprint
from flask import render_template


registration_blueprint = Blueprint(
    'registration', __name__, template_folder='templates',
)


@registration_blueprint.route('/', methods=['GET', 'POST'])
def view_registration_form():
    # Placeholder for profile
    return render_template('registration.tpl')
