import os
from flask import Flask, render_template, request, jsonify
import Thanos_voice_assistant  # Ensure this matches your assistant file

app = Flask(__name__)

# Retrieve API key from environment
api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    command = request.form.get('command')
    if not command:
        return jsonify({'response': 'No command received'}), 400
    
    response = Thanos_voice_assistant.respond_to_command(command, api_key)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
