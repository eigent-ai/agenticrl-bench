from flask import Blueprint, render_template
from models import db, Task, User

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
def dashboard():
    task_count = Task.query.count()
    user_count = User.query.count()
    return render_template('admin_dashboard.html', task_count=task_count, user_count=user_count)


@admin_bp.route('/users')
def users():
    all_users = User.query.all()
    return render_template('admin_dashboard.html', task_count=0, user_count=len(all_users))
