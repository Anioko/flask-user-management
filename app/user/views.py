from flask import Blueprint, render_template
from app.decorators import login_required

user_blueprint = Blueprint(
	'user',
	__name__,
	template_folder='templates'
)

@user_blueprint.route('/dashboard')
@login_required(role='user')
def dashboard():
	return render_template('user/dashboard.html')