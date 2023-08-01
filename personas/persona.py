import sys
import logging

import openai


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#MODEL = "gpt-3.5-turbo"
#MODEL = "gpt-3.5-turbo-0613"
MODEL = "gpt-4"
ROLE = "This is a social skills training program, which helps users rehearse new, often challenging social interactions. Convincingly roleplay a character that the user must learn to interact with. Roleplay instructions for your character and scene are in {{double brackets}}, but roleplaying actions are in *asterisk quotes*. When you respond to these instructions, out of character, put your responses in {{double brackets}} as well. Always stay in character. Follow all instructions."

BASE_MESSAGES=[
    {"role": "system", "content": ROLE },
]

class Persona:

    def __init__(self, name=None, scene=None, examples=None):
        self.base_messages = BASE_MESSAGES.copy()
        if scene:
            self.base_messages.append({"role": "user", "content": f"{{{{ {scene} }}}}"})
        if examples:
            self.base_messages += examples

        if name:
            self.reminder = " {{Respond as %s.}}" % name
        else:
            self.reminder = " {{Respond in character.}}"



    def fetch(self, messages):
        """takes a list of messages and returns chat output"""
        messages = messages[-20:]
        for message in messages:
            if(message["role"] == "user"):
                message["content"] = message["content"] + self.reminder
        input_messages = self.base_messages.copy() + messages

        logger.info(f"openai post: {input_messages}")

        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=input_messages
        )
        message = response['choices'][0]['message']

        logger.info(f"openai response: {message}")

        return message

basic_messages = [
    {"role": "user", "content": "Hello. *Waves.* {{Respond in character.}}" },
    {"role": "assistant", "content": "Hello. *Waves back.* How are you?" },
]
model_persona = Persona(examples=basic_messages)
