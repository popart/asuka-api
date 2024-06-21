import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request
from flask_cors import CORS
from flask import jsonify

from personas import asuka, grog, hermione, persona


# setup flask app
app = Flask(__name__)
CORS(app)

# setup logging
if os.getenv("DEBUG"):
    handler = RotatingFileHandler('./log/api.log', maxBytes=10000, backupCount=10)
    handler.setLevel(logging.INFO)

    root = logging.getLogger()
    root.addHandler(handler)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

personas = {
    "asuka": asuka.asuka,
    "grog": grog.grog,
    "hermione": hermione.persona,
    "custom": persona.model_persona,
}

@app.route('/', methods=['GET'])
def homepage():
    return 'Ack! What are you doing back here?!'

@app.route('/chat/<persona_name>', methods=['POST'])
def chat(persona_name):
    messages = request.json
    logger.info(f"{persona_name} - chat input messages: {messages}")
    persona = personas[persona_name]

    try:
        asst_message = persona.fetch(messages)
    except Exception as e:
        logger.error(e)
        return jsonify({"message": {"content": "<ERROR: CONNECTION INTERRUPTED>", "role": "assistant"}})

    return jsonify({"message": asst_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
