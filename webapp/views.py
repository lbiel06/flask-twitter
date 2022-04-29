from webapp import app, db
from webapp.models import User, Tweet
from flask import render_template, request, redirect, session, url_for
from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime

# Views

@app.route('/')
def home():
    tweets = sorted(Tweet.query.all(), key=lambda x: x.date, reverse=True)
    if 'user' in session:
        return render_template('home.html', 
            username=session['user'],
            tweets=tweets)

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username, password]):
            return render_template('login.html')
        
        if not (user := User.query.get(username)):
            return render_template('login.html')
        
        password_hash = user.password

        if checkpw(password.encode(), password_hash):
            session['user'] = username
            return redirect(url_for('home'))
        
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    else:
        username = request.form.get('username')
        password1 = request.form.get('password-1')
        password2 = request.form.get('password-2')

        if not all([username, password1, password2]):
            return render_template('register.html')
        
        if password1 != password2:
            return render_template('register.html')
        
        if User.query.get(username):
            return render_template('register.html')           

        password_hash = hashpw(password1.encode(), gensalt())
        new_user = User(username, password_hash, False)
        db.session.add(new_user)
        db.session.commit()
        print(new_user)
        return redirect(url_for('login'))


@app.route('/tweet', methods=['POST'])
def tweet():
    if 'user' in session:
        text = request.form.get('text')

        if not text:
            return redirect(url_for('home'))
        
        new_tweet = Tweet(session['user'], text, datetime.now())
        db.session.add(new_tweet)
        db.session.commit()
        print(new_tweet)
        return redirect(url_for('home'))

    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('login'))