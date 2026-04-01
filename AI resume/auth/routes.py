from flask import Blueprint, request, render_template, redirect, url_for, make_response
from models import db, User
from flask_bcrypt import Bcrypt
import jwt
import datetime
from flask import current_app

auth_bp = Blueprint('auth_bp', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.form
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and bcrypt.check_password_hash(user.password_hash, data.get('password')):
        token = jwt.encode({
            'user_id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        
        resp = make_response(redirect(url_for('dashboard')))
        resp.set_cookie('token', token, httponly=True, samesite='Strict')
        return resp
        
    return render_template('login.html', error='Invalid credentials')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.form
    password = data.get('password')
    username = data.get('username')
    email = data.get('email')

    if not all([username, email, password]):
        return render_template('register.html', error='All fields are required')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return render_template('register.html', error='Username already exists')
        
    new_user = User(username=username, email=email, password_hash=hashed_password, role='user')
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('auth_bp.login_page'))

@auth_bp.route('/logout')
def logout():
    resp = make_response(redirect(url_for('auth_bp.login_page')))
    resp.delete_cookie('token')
    return resp
