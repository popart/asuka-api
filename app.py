from flask import Flask, request
from flask_cors import CORS
from flask import jsonify

from transformers import RobertaForSequenceClassification, RobertaTokenizerFast, pipeline

import util
from personas import asuka, grog, persona


app = Flask(__name__)
CORS(app)

MODEL_NAME="j-hartmann/emotion-english-distilroberta-base"
TASK="text-classification"
model = RobertaForSequenceClassification.from_pretrained(f"models/{MODEL_NAME}")
tokenizer = RobertaTokenizerFast.from_pretrained(f"models/{MODEL_NAME}")
mood_classifier = pipeline(TASK, model=model, tokenizer=tokenizer, return_all_scores=True)

personas = {
    "asuka": asuka.asuka,
    "grog": grog.grog,
    "custom": persona.model_persona,
}

@app.route('/', methods=['GET'])
def homepage():
    return 'Ack! What are you doing back here?!'

@app.route('/chat/<persona_name>', methods=['POST'])
def chat(persona_name):
    messages = request.json
    app.logger.info(f"{persona_name} - chat input messages: {messages}")
    persona = personas[persona_name]

    try:
        asst_message = persona.fetch(messages)
        app.logger.info(f"asst response: {asst_message}")
    except Exception as e:
        print(e)
        return jsonify({"message": {"content": "<ERROR: CONNECTION INTERRUPTED>", "role": "assistant"}, "mood": "neutral"})


    try:
        asst_moods = mood_classifier(asst_message["content"])[0]
        asst_moods = sorted(asst_moods, key=lambda m: m["score"], reverse=True)
        app.logger.info(f"asst moods: {asst_moods}")
    except Exception as e:
        asst_moods = [{"label": "neutral", "score": 1.0}]

    # for now, just return top mood
    return jsonify({"message": asst_message, "mood": asst_moods[0]["label"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
