from flask import Flask, render_template, request, jsonify
from smartvoice import SmartVoice

app = Flask(__name__)
assistant = SmartVoice()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    text = request.json.get('text', '')
    response = assistant.generate_response(text)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)