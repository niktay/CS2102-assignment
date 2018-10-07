from flask import Blueprint
from flask import render_template


login_blueprint = Blueprint('login', __name__, template_folder='templates')


@login_blueprint.route('/', methods=['GET', 'POST'])
def view_login_form():
    # Placeholder for profile
    return render_template('login.tpl')
