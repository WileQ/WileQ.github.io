from flask import Flask, request, jsonify
import subprocess
import sys
import io

app = Flask(__name__)

# Whitelisted imports for dynamic execution
allowed_imports = {
    "numpy" : "import numpy"
}


@app.route('/run', methods=['POST'])
def run_python_script():
    try:
        data = request.get_json()
        code = data.get('code', '')

        # Prepare the execution context
        exec_context = {}

        # Handle allowed imports
        for module_name, import_statement in allowed_imports.items():
            exec(import_statement, exec_context)

        # Capture output
        stdout_backup = sys.stdout
        sys.stdout = io.StringIO()  # Redirect stdout to capture print statements

        try:
            exec(code, exec_context)  # Execute the user code in the custom context
            output = sys.stdout.getvalue()  # Get captured output
        finally:
            sys.stdout = stdout_backup  # Restore stdout

        return jsonify({
            'output': output,
            'error': ''
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
