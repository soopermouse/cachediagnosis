# cachemed/app.py
import os
from flask import Flask
from flask_cors import CORS

# Import blueprints
from api import api_bp

# Initialize app
app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(api_bp)

@app.route('/')
def index():
    return {'message': 'Cachemed API', 'version': '1.0.0'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)