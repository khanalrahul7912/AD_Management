from flask import Blueprint, render_template, session
from app.decorators import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    """Dashboard/home page"""
    return render_template('index.html', username=session.get('username'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html', username=session.get('username'))
