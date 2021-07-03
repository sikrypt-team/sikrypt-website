from app import db 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	score = db.Column(db.Integer,default=0)
	password = db.Column(db.String(128),unique=True)


	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self,pwd):
		self.password = generate_password_hash(pwd)
		
	def check_password(self,pwd):
		return check_password_hash(self.password,pwd)



@login.user_loader
def load_user(id):
	return User.query.get(int(id)) 


class Hunt(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	question = db.Column(db.String(1000))
	ans = db.Column(db.String(1000))
