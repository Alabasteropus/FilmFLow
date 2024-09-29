# src/routes/scripts.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.script_service import (
    create_script, get_user_scripts, get_script_by_id, update_script, delete_script
)
from ..services.auth_service import get_user
from ..schemas.script_schema import ScriptSchema
from marshmallow import ValidationError
import logging

scripts_bp = Blueprint('scripts', __name__)

@scripts_bp.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {e}")
    return jsonify({'error': 'An internal error occurred.'}), 500

@scripts_bp.route('/', methods=['POST'])
@jwt_required()
def create_new_script():
    current_user_username = get_jwt_identity()
    user = get_user(current_user_username)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    data = request.get_json()
    schema = ScriptSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    title = validated_data['title']
    content = validated_data['content']

    try:
        script = create_script(user.id, title, content)
        return jsonify(script.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@scripts_bp.route('/', methods=['GET'])
@jwt_required()
def list_scripts():
    current_user_username = get_jwt_identity()
    user = get_user(current_user_username)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    scripts = get_user_scripts(user.id)
    scripts_data = [script.to_dict() for script in scripts]

    return jsonify({'scripts': scripts_data}), 200

@scripts_bp.route('/<int:script_id>', methods=['GET'])
@jwt_required()
def get_script(script_id):
    current_user_username = get_jwt_identity()
    user = get_user(current_user_username)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    script = get_script_by_id(script_id, user.id)
    if not script:
        return jsonify({'error': 'Script not found.'}), 404

    return jsonify(script.to_dict()), 200

@scripts_bp.route('/<int:script_id>', methods=['PUT'])
@jwt_required()
def edit_script_route(script_id):
    current_user_username = get_jwt_identity()
    user = get_user(current_user_username)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    data = request.get_json()
    schema = ScriptSchema(partial=True)  # Allow partial updates
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    title = validated_data.get('title')
    content = validated_data.get('content')

    if not title and not content:
        return jsonify({'error': 'At least one of title or content must be provided.'}), 400

    try:
        script = update_script(script_id, user.id, title, content)
        return jsonify(script.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@scripts_bp.route('/<int:script_id>', methods=['DELETE'])
@jwt_required()
def delete_script_route(script_id):
    current_user_username = get_jwt_identity()
    user = get_user(current_user_username)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    try:
        delete_script(script_id, user.id)
        return jsonify({'message': 'Script deleted successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404
