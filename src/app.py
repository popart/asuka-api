import os
import logging
from logging.handlers import RotatingFileHandler

import flask
import flask_cors
from flask import jsonify

from google.oauth2 import id_token
from google.auth.transport import requests

from dotenv import load_dotenv
load_dotenv()  # take environment variables from local .env

from personas import asuka, grog, hermione, sensei, persona
from clients.openai_client import OpenAIClient
from clients.anthropic_client import AnthropicClient


# setup from env
SESSION_SECRET_KEY = os.environ["SESSION_SECRET_KEY"]
GOOGLE_OAUTH_CLIENT_ID = os.environ["GOOGLE_OAUTH_CLIENT_ID"]
ENV = os.getenv("ENV", "local")

# setup flask app
app = flask.Flask(__name__)
app.secret_key = SESSION_SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 4 * 1000 * 1000  # 4 MB

flask_cors.CORS(app, supports_credentials=True)

if ENV == "gcp":
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_DOMAIN"] = "goginko.com"

# setup logging
if os.getenv("DEBUG"):
    handler = RotatingFileHandler('./log/api.log', maxBytes=10000, backupCount=10)
    handler.setLevel(logging.INFO)

    root = logging.getLogger()
    root.addHandler(handler)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ai_client = OpenAIClient()
#ai_client = AnthropicClient(model="claude-3-haiku-20240307")

personas = {
    "asuka": persona.Persona(ai_client, **asuka.persona),
    "grog": persona.Persona(ai_client, **grog.persona),
    "hermione": persona.Persona(ai_client, **hermione.persona),
    "sensei": persona.Persona(ai_client, **sensei.persona),
    "custom": persona.Persona(ai_client),
}

@app.route('/', methods=['GET'])
def homepage():
    return 'Ack! What are you doing back here?!'

@app.route("/login", methods=["POST"])
def login():
    data = flask.request.json
    token = data.get("token") if data else None

    # Verify the token here using Google's library or any other method
    try:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), GOOGLE_OAUTH_CLIENT_ID
        )
        openid_sub = idinfo["sub"]
        openid_email = idinfo["email"]

        # create a session! this will create a session token
        flask.session["openid_sub"] = openid_sub
        flask.session["openid_email"] = openid_email

        return (
            flask.jsonify({
                "message": "Token is valid",
            }),
            200,
        )

    except ValueError as e:
        return flask.jsonify({"message": str(e)}), 400

@app.route("/check_login", methods=["GET", "POST"])
def check_login():
    is_logged_in = flask.session.get("openid_email") is not None
    return flask.jsonify({"loggedIn": is_logged_in}), 200


@app.route("/logout", methods=["POST"])
def logout():
    flask.session.clear()  # This clears the entire session
    return flask.jsonify({"message": "Logged out successfully"}), 200

@app.route('/chat/<persona_name>', methods=['POST'])
def chat(persona_name):
    current_user_email = flask.session.get("openid_email")

    messages = flask.request.json
    logger.info(f"{persona_name} - chat input messages: {messages}")
    persona = personas[persona_name]

    try:
        asst_message = persona.fetch(messages)
    except Exception as e:
        logger.error(e)
        return jsonify({"message": {"content": "<ERROR: CONNECTION INTERRUPTED>", "role": "assistant"}})

    return jsonify({"message": asst_message, "email": current_user_email})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
