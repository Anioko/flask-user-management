from sqlalchemy.sql import func
from flask_login import UserMixin
from app import app, db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# Database models
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(255), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	role = db.Column(db.String(255), nullable=False)
	date_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

	def get_reset_token(self, expires_sec=1800):
		serializer = Serializer(app.config['SECRET_KEY'], expires_sec)
		return serializer.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		serializer = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = serializer.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __init__(self, name, email, password, role):
		self.name = name
		self.email = email
		self.password = password
		self.role = role