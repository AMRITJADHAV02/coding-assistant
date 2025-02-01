from flask import Flask, request, jsonify, send_from_directory
import subprocess
import re

app = Flask(__name__)

# Function to clean and format the model's response
def clean_response(response):
    # Replace problematic characters (e.g., â€™ with ’)
    response = response.replace("â€™", "’")
    response = response.replace("â€œ", "“")
    response = response.replace("â€", "”")
    response = response.replace("â€˜", "‘")
    response = response.replace("â€”", "—")
    
    # Ensure code blocks are wrapped in <pre><code> tags for proper rendering in HTML
    response = re.sub(r"```(.*?)```", r"<pre><code>\1</code></pre>", response, flags=re.DOTALL)
    
    # Replace newlines with <br> tags for HTML rendering
    response = response.replace("\n", "<br>")
    
    return response

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

    # Clean and format the response
    cleaned_response = clean_response(result.stdout)

    # Return the response
    return jsonify({"response": cleaned_response})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)