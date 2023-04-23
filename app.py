from flask import Flask, request
from flask_cors import CORS
from flask import jsonify

from transformers import pipeline

from personas import asuka

app = Flask(__name__)
CORS(app)

mood_classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    # do something with the data here
    response = asuka.fetch(data)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
