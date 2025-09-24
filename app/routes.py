from datetime import datetime, timezone
import os
from urllib.parse import urlsplit
from flask import current_app, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import requests
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
   
    return render_template('index.html', title='Home', )

@app.route("/facility_locator")
def facility_locator():
    api_key = current_app.config["GOOGLE_MAPS_API_KEY"]
    return render_template("facility_locator.html", api_key=api_key)

@app.route('/sha-claims')
@login_required
def sha_claims():
    return render_template('sha_claims.html')

@app.route('/maternal-child')
@login_required
def maternal_child():
    return render_template('maternal_child.html')

@app.route('/health-education')
@login_required
def health_education():
    return render_template('health_education.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    response = None
    if request.method == 'POST':
        user_input = request.form['prompt']
        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile", #  model="llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        }
        try:
            res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
            res.raise_for_status()
            response = res.json()['choices'][0]['message']['content']
        except requests.exceptions.HTTPError:
            # Print error details for debugging
            response = f"Error: {res.status_code} - {res.text}"
        except Exception as e:
            response = f"Error: {str(e)}"
    return render_template('chat.html', response=response)
