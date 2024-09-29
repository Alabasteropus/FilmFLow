# src/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from marshmallow import ValidationError
from ..services.auth_service import register_user, login_user, get_user
from ..schemas.user_schema import UserSchema
import logging

auth_bp = Blueprint('auth', __name__)

@auth_bp.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {e}")
    return jsonify({'error': 'An internal error occurred.'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    schema = UserSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    username = validated_data['username']
    password = validated_data['password']
    try:
        register_user(username, password)
        return jsonify({'message': 'User registered successfully.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    schema = UserSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    username = validated_data['username']
    password = validated_data['password']
    if login_user(username, password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials.'}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}! This is a protected route.'}), 200
