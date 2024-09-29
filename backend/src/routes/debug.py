# src/routes/debug.py
from flask import Blueprint, jsonify
import os

debug_bp = Blueprint('debug', __name__)

@debug_bp.route('/debug/env', methods=['GET'])
def debug_env():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    jwt_secret_key = os.getenv('JWT_SECRET_KEY')
    return jsonify({
        "OPENAI_API_KEY": "Loaded" if openai_api_key else "Not Loaded",
        "JWT_SECRET_KEY": "Loaded" if jwt_secret_key else "Not Loaded"
    }), 200
