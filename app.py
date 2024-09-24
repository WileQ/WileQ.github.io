from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import subprocess


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/run', methods=['POST'])
def run_python_script():
    try:
        data = request.json
        code = data.get('code', '')
        result = subprocess.run(['python', '-c', code], capture_output=True, text=True)
        return jsonify({
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run()

