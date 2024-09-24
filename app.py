from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_python_script():
    try:
        # Get the Python code from the incoming request
        data = request.json
        code = data.get('code', '')

        # Execute the Python code using subprocess
        result = subprocess.run(['python', '-c', code], capture_output=True, text=True)

        # Return the result
        return jsonify({
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # This is just for local testing
    app.run(debug=True)
