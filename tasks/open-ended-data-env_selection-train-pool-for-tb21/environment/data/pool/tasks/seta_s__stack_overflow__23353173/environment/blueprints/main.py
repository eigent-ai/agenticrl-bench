from flask import Blueprint, render_template, jsonify
from models import db, Task

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/tasks')
def tasks():
    all_tasks = Task.query.all()
    return jsonify([t.to_dict() for t in all_tasks])


@main_bp.route('/dashboard')
def dashboard():
    task_count = Task.query.count()
    return render_template('user_dashboard.html', task_count=task_count)
