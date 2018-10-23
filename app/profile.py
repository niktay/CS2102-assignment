from flask import Blueprint
from flask import render_template
from flask_login import login_required

profile_blueprint = Blueprint('profile', __name__, template_folder='templates')


@profile_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def view_profile():
    return render_template('profile.tpl')
