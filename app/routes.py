from flask import *
from app import app
from app import db
from app.forms import LoginForm
from flask_login import current_user,login_user,logout_user
from app.models import User,Hunt
from app.forms import RegForm,fpass_form,HuntForm


def get_leaderboard():
	query = db.session.query(User).order_by(User.score.desc())
	users = query.all() 
	return users

@app.route('/')
#@login_required
def home_page():
	users = get_leaderboard()
	return render_template('home.html',ulist=users)




@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		level = current_user.score + 1
		level = str(level)
		return redirect('/hunt/' + level)
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user,remember=form.remember_me.data)
		return redirect(url_for('idea'))
	return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		redirect(url_for('login'))
	form = RegForm()
	if form.validate_on_submit():
		user=User(username=form.username.data,email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You are now a registered user')
		return redirect(url_for('login'))
	return render_template('register.html',form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))
	
@app.route('/fpass',methods=['GET','POST'])
def fpass():
	if current_user.is_authenticated:
		redirect(url_for('home_page'))
	form = fpass_form()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_email()

	return render_template('fpass.html',form=form)

@app.route('/idea',methods=['GET','POST'])
def idea():
	if current_user.is_anonymous:
		redirect(url_for('login'))
	question = Hunt.query.filter_by(id=1).first()
	form = HuntForm()
	if form.validate_on_submit():
		ans = Hunt.query.filter_by(id=1).first()
		usr_id = current_user.id
		user = User.query.filter_by(id=usr_id).first()

		if ans.ans == form.ans.data:
			user.score = 1
			db.session.commit()
			return redirect('/hunt/2')

	return render_template('quiz.html',form=form,question=question.question)

@app.route('/reality')
def reality():
	return render_template('reality_l1.htm')
	
@app.route('/hunt/<level>',methods=['GET','POST'])
def hunt(level):
	if current_user.is_anonymous:
		redirect(url_for('login'))
	question = Hunt.query.filter_by(id=level).first()
	form = HuntForm()
	if form.validate_on_submit():
		ans = Hunt.query.filter_by(id=level).first()
		usr_id = current_user.id
		user = User.query.filter_by(id=usr_id).first()

		if ans.ans == form.ans.data:
			next_level = int(level) + 1
			next_level = str(next_level)
			user.score = level
			db.session.commit()
			return redirect(next_level)

	return render_template('quiz.html',form=form,question=question.question,level=level)






