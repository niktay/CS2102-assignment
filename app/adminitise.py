from flask import Blueprint
from flask import render_template
from flask import request
from model.adminitise import Adminitise

adminitise_blueprint = Blueprint(
    'adminitise', __name__, template_folder='templates',
)


@adminitise_blueprint.route('/create', methods=['GET', 'POST'])
def view_doneAdminitised():

    if request.method != 'POST':
        return render_template('adminitise.tpl')

    new_admin = Adminitise(**request.form)
    is_success = False

    try:
        print(new_admin)
        made_new_admin = new_admin.save()
        is_success = made_new_admin
    except Exception as e:
        print(e)

    return render_template(
        'adminitise.tpl', is_view=True,
        is_success=is_success,
    )


@adminitise_blueprint.route('/', methods=['GET'])
def view_adminitise():
    return render_template('adminitise.tpl', is_view=False)
