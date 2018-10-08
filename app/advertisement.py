from flask import Blueprint
from flask import render_template


advertisement_blueprint = Blueprint(
    'advertisement', __name__, template_folder='templates',
)


@advertisement_blueprint.route('/', methods=['GET', 'POST'])
def view_advertisement_form():
    # Placeholder for profile
    return render_template('advertisement.tpl')
