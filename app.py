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
    app.logger.info(f"chat input messages: {messages}")

    for message in messages:
        message["content"] = util.remove_chevrons(message["content"])

    try:
        asuka_message = asuka.fetch(messages)
        app.logger.info(f"asuka response: {asuka_message}")
    except Exception as e:
        return jsonify({"message": "<ERROR: CONNECTION INTERRUPTED>", "mood": "neutral"})


    try:
        asuka_mood = mood_classifier(asuka_message["content"])
        app.logger.info(f"asuka mood: {asuka_mood}")
    except Exception as e:
        asuka_mood = [{"label": "neutral"}]

    return jsonify({"message": asuka_message, "mood": asuka_mood[0]["label"]})

if __name__ == '__main__':
    app.run(debug=True)
