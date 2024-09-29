# run.py
import sys
from pathlib import Path
from flask.cli import FlaskGroup

from src import create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        # Run the Flask development server
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        # Invoke the Flask CLI (e.g., db commands)
        cli()
