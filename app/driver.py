import psycopg2
from flask import Flask
from flask import render_template
from flask import request
from flask import Blueprint


driver_blueprint = Blueprint('drivers', __name__, template_folder = 'templates')

@driver_blueprint.route('/driver', methods=['GET', 'POST'])
def view_profile():
    # Placeholder for profile
    return render_template('driver.tpl')
