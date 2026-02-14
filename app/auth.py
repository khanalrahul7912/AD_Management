from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.ad_manager import get_ad_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password.', 'danger')
            return render_template('auth/login.html')
        
        # Try to authenticate with AD
        ad_conn = get_ad_connection(username, password)
        if ad_conn:
            # Successfully authenticated
            session['username'] = username
            session['password'] = password  # Store for subsequent AD operations
            
            # Check if user is admin (member of Domain Admins or similar)
            try:
                user = ad_conn.get_user(username)
                if user and 'memberOf' in user:
                    member_of = user.memberOf.values if hasattr(user.memberOf, 'values') else [user.memberOf.value]
                    # Check for admin groups
                    is_admin = any('Domain Admins' in group or 'Administrators' in group for group in member_of)
                    session['is_admin'] = is_admin
                else:
                    session['is_admin'] = False
            except:
                session['is_admin'] = False
            
            ad_conn.disconnect()
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Logout handler"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}!', 'info')
    return redirect(url_for('auth.login'))
