from flask import send_from_directory
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Get the user's message
    user_input = request.json.get("message")

    # Use Ollama to generate a response
    command = f'ollama run deepseek-r1:1.5b "{user_input}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Return the response
    return jsonify({"response": result.stdout})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)