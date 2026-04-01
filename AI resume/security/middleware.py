from functools import wraps
from flask import request, jsonify, current_app, redirect, url_for
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        
        if not token:
            return redirect(url_for('auth_bp.login_page'))
            
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user_id']
            user_role = data.get('role', 'user')
        except:
            return redirect(url_for('auth_bp.login_page'))
            
        return f(*args, current_user=current_user, user_role=user_role, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_role = kwargs.get('user_role')
        if user_role != 'admin':
            return jsonify({'message': 'Admin access required!'}), 403
        return f(*args, **kwargs)
    return decorated
