from flask import Blueprint, jsonify, request
from src.middleware.auth import require_auth

protected_bp = Blueprint('protected', __name__)


@protected_bp.route('/api/profile', methods=['GET', 'PUT', 'DELETE'])
@require_auth
def profile():
    if request.method == 'GET':
        return jsonify({
            'user': request.user_data['username'],
            'message': 'Profile data'
        })
    elif request.method == 'PUT':
        return jsonify({'message': 'Profile updated'})
    elif request.method == 'DELETE':
        return jsonify({'message': 'Profile deleted'})


@protected_bp.route('/api/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
@require_auth
def data():
    return jsonify({
        'message': f'Data endpoint accessed via {request.method}'
    })
