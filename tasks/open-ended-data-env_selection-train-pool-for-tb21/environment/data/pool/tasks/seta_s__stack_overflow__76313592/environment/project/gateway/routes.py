from flask import Blueprint, jsonify, request
from datavalidator import Validator

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    validator = Validator()
    try:
        result = validator.validate(data)
        return jsonify({"valid": True, "data": result})
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 422
