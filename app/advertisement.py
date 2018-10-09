from flask import Blueprint
from flask import render_template
from flask import request
from model import Advertisement
# from model import Driver


advertisement_blueprint = Blueprint(
    'advertisement', __name__, template_folder='templates',
)


@advertisement_blueprint.route('/create', methods=['GET', 'POST'])
def create_advertisement_form():
    if request.method != 'POST':
        return render_template('advertisement.tpl')

    new_advertisement = Advertisement(**request.form)
    is_success = False
    try:
        print(new_advertisement)
        is_advertisement_store = new_advertisement.save()
        print(is_advertisement_store)
        is_success = new_advertisement and is_advertisement_store

    except Exception as e:
        print(e)

    return render_template('advertisement', is_view=True, is_succes=is_success)


@advertisement_blueprint.route('/', method=['GET'])
def view_advertisement_creation():
    return render_template('advertisement.tpl', is_view=False)
