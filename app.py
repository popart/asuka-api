from flask import Flask, request
from flask_cors import CORS
from flask import jsonify

from transformers import RobertaForSequenceClassification, RobertaTokenizerFast, pipeline

import util
from personas import asuka

app = Flask(__name__)
CORS(app)

MODEL_NAME="j-hartmann/emotion-english-distilroberta-base"
TASK="text-classification"
model = RobertaForSequenceClassification.from_pretrained(f"models/{MODEL_NAME}")
tokenizer = RobertaTokenizerFast.from_pretrained(f"models/{MODEL_NAME}")
mood_classifier = pipeline(TASK, model=model, tokenizer=tokenizer, return_all_scores=True)

@app.route('/', methods=['GET'])
def homepage():
    return 'Ach! Get out of here!'

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
        print(e)
        return jsonify({"message": {"content": "<ERROR: CONNECTION INTERRUPTED>", "role": "assistant"}, "mood": "neutral"})


    try:
        asuka_moods = mood_classifier(asuka_message["content"])[0]
        asuka_moods = sorted(asuka_moods, key=lambda m: m["score"], reverse=True)
        app.logger.info(f"asuka moods: {asuka_moods}")
    except Exception as e:
        asuka_moods = [{"label": "neutral", "score": 1.0}]

    # for now, just return top mood
    return jsonify({"message": asuka_message, "mood": asuka_moods[0]["label"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
