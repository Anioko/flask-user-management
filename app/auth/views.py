from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.auth.forms import (LoginForm, SignupForm,
							RequestResetForm, ResetPasswordForm)
from app.reset_password import send_reset_email
from app.url_endpoint import redirect_dest
from app.models import User
from app import db, bcrypt

auth_blueprint = Blueprint(
	'auth',
	__name__,
	template_folder='templates'
)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
	# If user is already authenticated redirect to designated page
	if current_user.is_authenticated and current_user.role == 'admin':
		return redirect_dest(fallback=url_for('admin.dashboard'))
	elif current_user.is_authenticated and current_user.role == 'user':
		return redirect_dest(fallback=url_for('user.dashboard'))

	form = LoginForm()

	if request.method == 'POST' and form.validate():
		email = request.form['email']
		password = request.form['password']
		user = User.query.filter_by(email=email).first()

		if user and bcrypt.check_password_hash(user.password, password) and user.role == 'admin':
			login_user(user, remember=form.remember.data)
			return redirect_dest(fallback=url_for('admin.dashboard'))
		elif user and bcrypt.check_password_hash(user.password, password) and user.role == 'user':
			login_user(user, remember=form.remember.data)
			return redirect_dest(fallback=url_for('user.dashboard'))
		else:
			flash('Login failed! Your email or password is incorrect.', 'danger')
	return render_template('auth/login.html', form=form)

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
	# If user is already authenticated redirect to designated page
	if current_user.is_authenticated and current_user.role == 'admin':
		return redirect_dest(fallback=url_for('admin.dashboard'))
	elif current_user.is_authenticated and current_user.role == 'user':
		return redirect_dest(fallback=url_for('user.dashboard'))
		
	form = SignupForm()

	if request.method == 'POST' and form.validate():
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		role = 'user'
		
		hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
		user = User(name=name, email=email, password=hashed_password, role=role)

		db.session.add(user)
		db.session.commit()

		flash('Success! Your account has been created.', 'success')
		return redirect(url_for('auth.login'))
	return render_template('auth/signup.html', form=form)

@auth_blueprint.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

@auth_blueprint.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
	# If user is already authenticated redirect to designated page
	if current_user.is_authenticated and current_user.role == 'admin':
		return redirect_dest(fallback=url_for('admin.dashboard'))
	elif current_user.is_authenticated and current_user.role == 'user':
		return redirect_dest(fallback=url_for('user.dashboard'))

	form = RequestResetForm()

	if request.method == 'POST' and form.validate():
		email = request.form['email']
		user = User.query.filter_by(email=email).first()
		send_reset_email(user)
		flash('A message has been sent to your email with instructions to reset your password.', 'info')
		return redirect(url_for('auth.login'))
	return render_template('auth/request_reset.html', form=form)

@auth_blueprint.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	# If user is already authenticated redirect to designated page
	if current_user.is_authenticated and current_user.role == 'admin':
		return redirect_dest(fallback=url_for('admin.dashboard'))
	elif current_user.is_authenticated and current_user.role == 'user':
		return redirect_dest(fallback=url_for('user.dashboard'))

	user = User.verify_reset_token(token)

	if user is None:
		flash('Invalid or expired token, please try again!', 'warning')
		return redirect(url_for('auth.reset_request'))

	form = ResetPasswordForm()

	if request.method == 'POST' and form.validate():
		password = request.form['password']

		hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
		user.password = hashed_password

		db.session.commit()

		flash('Success! Your password has been updated.', 'success')
		return redirect(url_for('auth.login'))
	return render_template('auth/request_token.html', form=form)