# src/routes/generate_text.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.openai_service import generate_text
import logging

generate_text_bp = Blueprint('generate_text', __name__)

@generate_text_bp.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {e}")
    return jsonify({'error': 'An internal error occurred.'}), 500

@generate_text_bp.route('/generate-text', methods=['POST'])
@jwt_required()
def generate_text_route():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({'error': 'Prompt is required.'}), 400

    prompt = data['prompt']
    try:
        generated = generate_text(prompt)
        return jsonify({'generated_text': generated}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
