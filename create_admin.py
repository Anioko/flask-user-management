from app import app, db, bcrypt
from app.models import User
from sqlalchemy.exc import SQLAlchemyError

password = bcrypt.generate_password_hash('admin123').decode('utf-8')
user = User(
	name='Administrator',
	email='admin@demo.com',
	password=password,
	role='admin'
)

def db_commit():
	try:
		db.session.commit()
		print('Administrator account has been created!')
		return True
	except SQLAlchemyError:
		result = str(SQLAlchemyError)
		print(result)
		return False

with app.app_context():
	if db_commit():
		db.session.add(user)
		db.session.commit()