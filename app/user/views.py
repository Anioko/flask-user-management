from flask import Blueprint, render_template, redirect, request, url_for, flash
from app.decorators import login_required
from flask_login import current_user
from app.models import User
from app import db, bcrypt

user_blueprint = Blueprint(
	'user',
	__name__,
	template_folder='templates'
)

@user_blueprint.route('/dashboard')
@login_required(role='user')
def dashboard():
	return render_template('user/dashboard.html')

@user_blueprint.route('/account-settings/<int:id>')
@login_required(role='user')
def account_settings(id):
	user = User.query.filter(User.id == current_user.id).filter_by(id=id)
	return render_template('user/account_settings.html', user=user)

@user_blueprint.route('/update-name/<int:id>', methods=['GET', 'POST'])
@login_required(role='user')
def update_name(id):
	if request.method == 'POST':
		user = User.query.get_or_404(id)
		user.name = request.form['name']

		db.session.commit()

		flash('Your account name has been updated successfully!', 'success')
		return redirect(url_for('user.account_settings', id=id))
	return redirect(url_for('user.dashboard'))

@user_blueprint.route('/change-password/<int:id>', methods=['GET', 'POST'])
@login_required(role='user')
def change_password(id):
	if request.method == 'POST':
		user = User.query.get_or_404(id)
		password = request.form['password']
		confirm_password = request.form['confirm_password']

		if password != confirm_password:
			flash('Password and confirm password do not match, please try again!', 'danger')
			return redirect(url_for('user.account_settings', id=id))
		elif len(password) < 6 or len(password) > 32:
			flash('Password field must be between 6 and 32 characters long.', 'danger')
			return redirect(url_for('user.account_settings', id=id))
		else:
			user.password = bcrypt.generate_password_hash(password).decode('utf-8')
			db.session.commit()

		flash('Password has been changed successfully!', 'success')
		return redirect(url_for('user.account_settings', id=id))
	return redirect(url_for('user.dashboard'))

@user_blueprint.route('/delete-account/<int:id>', methods=['GET', 'POST'])
@login_required(role='user')
def delete_account(id):
	if request.method == 'POST':
		user = User.query.get_or_404(id)

		db.session.delete(user)
		db.session.commit()

		flash('Your account has been deleted successfully!', 'success')
		return redirect(url_for('auth.login'))
	return redirect(url_for('user.dashboard'))