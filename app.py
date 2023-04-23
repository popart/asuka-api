from flask import Flask, request
from flask_cors import CORS
from flask import jsonify

from transformers import pipeline

import util
from personas import asuka

app = Flask(__name__)
CORS(app)

mood_classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")

@app.route('/chat', methods=['POST'])
def chat():
    messages = request.json
    for message in messages:
        message["content"] = util.remove_chevrons(message["content"])

    asuka_message = asuka.fetch(messages)
    asuka_mood = mood_classifier(asuka_message["content"])
    return jsonify({"message": asuka_message, "mood": asuka_mood[0]["label"]})

if __name__ == '__main__':
    app.run(debug=True)
