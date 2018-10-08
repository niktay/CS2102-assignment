from flask import Blueprint
from flask import render_template


createAd_blueprint = Blueprint(
    'advertisement', __name__, template_folder='templates',
)


@createAd_blueprint.route('/', methods=['GET', 'POST'])
def view_createAd_form():
    # Placeholder for profile
    return render_template('createAd.tpl')
