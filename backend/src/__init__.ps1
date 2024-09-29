# app.py
from flask import Flask, request, jsonify
import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import logging
from flask_cors import CORS

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the /generate-text endpoint
CORS(app, resources={r"/generate-text": {"origins": "http://localhost:3000"}})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')  # Ensure this environment variable is set
)

# Verify that the API key is loaded
if not client.api_key:
    logger.error("OpenAI API key not found. Please set OPENAI_API_KEY in the .env file.")
    raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in the .env file.")

@app.route('/generate-text', methods=['POST'])
def generate_text():
    """
    Generates text based on the provided prompt using OpenAI's Chat Completion API.
    Expects a JSON payload with a 'prompt' field.
    """
    data = request.get_json()

    if not data or 'prompt' not in data:
        logger.warning("No prompt provided in the request.")
        return jsonify({'error': 'No prompt provided.'}), 400

    prompt = data.get('prompt').strip()
    logger.info(f"Received prompt: {prompt}")

    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',  # Use 'gpt-4' if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None
        )

        generated_text = response.choices[0].message.content.strip()
        logger.info(f"Generated text: {generated_text}")

        return jsonify({'generated_text': generated_text})

    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        return jsonify({'error': f'OpenAI API error: {e}'}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

@app.errorhandler(404)
def not_found(e):
    """
    Custom 404 error handler.
    """
    return jsonify({'error': 'Endpoint not found.'}), 404

@app.errorhandler(500)
def internal_error(e):
    """
    Custom 500 error handler.
    """
    return jsonify({'error': 'Internal server error.'}), 500

if __name__ == '__main__':
    # Run the app with debug mode enabled and on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
