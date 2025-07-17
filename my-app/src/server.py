from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import sys

app = Flask(__name__)
CORS(app)  # ✅ Allows React to communicate with Flask

@app.route('/run-reading-assistant', methods=['GET'])
def run_reading_assistant():
    try:
        # ✅ Use sys.executable to ensure correct Python version
        subprocess.run([sys.executable, "reading_assistant.py"], check=True)
        return jsonify({"message": "Reading Assistant started successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
