from flask import Blueprint
from flask import render_template
from flask import request
from model import Account

adminitise_blueprint = Blueprint(
    'adminitise', __name__, template_folder='templates',
)


@adminitise_blueprint.route('/create', methods=['GET', 'POST'])
def adminitise_account():

    if request.method != 'POST':
        return render_template('adminitise.tpl')

    account = Account.load(request.form.get('username', 'None'))

    toggle_success = False
    if account:
        toggle_success = account.toggle_admin_status()

    return render_template(
        'adminitise.tpl', is_view=True,
        is_success=toggle_success,
    )


@adminitise_blueprint.route('/', methods=['GET'])
def view_adminitise():
    return render_template('adminitise.tpl', is_view=False)
