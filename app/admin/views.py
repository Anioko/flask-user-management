from flask import Blueprint, render_template, redirect, request, url_for, flash
from app.admin.forms import CreateAccountForm
from app.decorators import login_required
from app.models import User
from app import db, bcrypt

admin_blueprint = Blueprint(
	'admin',
	__name__,
	template_folder='templates'
)

@admin_blueprint.route('/dashboard')
@login_required(role='admin')
def dashboard():
	return render_template('admin/dashboard.html')

@admin_blueprint.route('/user-management')
@login_required(role='admin')
def user_management():
	users = User.query.all()
	return render_template('admin/user_management.html', users=users)

@admin_blueprint.route('/create-account', methods=['GET', 'POST'])
@login_required(role='admin')
def create_account():
	form = CreateAccountForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			name = request.form['name']
			email = request.form['email']
			password = request.form['password']
			role = form.user_type.data
			
			hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
			user = User(name=name, email=email, password=hashed_password, role=role)

			db.session.add(user)
			db.session.commit()

			flash('Success! Account has been created.', 'success')
			return redirect(url_for('admin.user_management'))
	return render_template('admin/create_account.html', form=form)

@admin_blueprint.route('/update-account/<int:id>', methods=['GET'])
@login_required(role='admin')
def update_account(id):
	user = User.query.filter_by(id=id)
	return render_template('admin/update_account.html', user=user)

@admin_blueprint.route('/update-name/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def update_name(id):
	if request.method == 'POST':
		user = User.query.get_or_404(id)
		user.name = request.form['name']

		db.session.commit()

		flash('Success! Account name has been updated.', 'success')
		return redirect(url_for('admin.update_account', id=id))
	return redirect(url_for('admin.user_management'))

@admin_blueprint.route('/change-password/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def change_password(id):
	if request.method == 'POST':
			user = User.query.get_or_404(id)
			password = request.form['password']
			confirm_password = request.form['confirm_password']

			if password != confirm_password:
				flash('Failed! Password does NOT match, please try again!', 'danger')
				return redirect(url_for('admin.update_account', id=id))
			else:
				user.password = bcrypt.generate_password_hash(password).decode('utf-8')
				db.session.commit()

			flash('Success! Password has been changed.', 'success')
			return redirect(url_for('admin.update_account', id=id))
	return redirect(url_for('admin.user_management'))

@admin_blueprint.route('/user-management/delete/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def delete_user(id):
	if request.method == 'POST':
		user = User.query.get_or_404(id)

		db.session.delete(user)
		db.session.commit()

		flash('Success! User has been deleted.', 'success')
		return redirect(url_for('admin.user_management'))
	return redirect(url_for('admin.user_management'))