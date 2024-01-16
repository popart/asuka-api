import sys
import logging
import uuid

from openai import OpenAI

client = OpenAI()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#MODEL = "gpt-3.5-turbo"
#MODEL = "gpt-4"
MODEL = "gpt-4-1106-preview" # gpt-4 turbo

BASE_ROLE = ""
BASE_COMPLIANCE = ""

class Persona:

    def __init__(self, name=None, role=None, examples=None):
        self.base_messages = []
        if role:
            self.base_messages.append({"role": "system", "content": role })
        else:
            self.base_messages.append({"role": "system", "content": BASE_ROLE })
            #self.base_messages.append({"role": "assistant", "content": BASE_COMPLIANCE })


        if examples:
            self.base_messages += examples


    def fetch(self, messages):
        """takes a list of messages and returns chat output"""
        # check for instruction messages
        system_messages = []
        chat_messages = []
        for m in messages:
            if m["content"].startswith("{{") and m["content"].endswith("}}"):
                m["role"] = "system"
                m["content"] = m["content"][2:-2]
                system_messages.append(m)
            else:
                chat_messages.append(m)

        messages = system_messages + chat_messages[-40:]
            
        input_messages = self.base_messages.copy() + messages

        logger.info(f"openai post: {input_messages}")

        response = client.chat.completions.create(
            model=MODEL,
            messages=input_messages,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            temperature=0.5,
            user=str(uuid.uuid4())
        )

        message = {
            "content": response.choices[0].message.content,
            "role": response.choices[0].message.role,
        }

        logger.info(f"openai response: {message}")

        return message

model_persona = Persona()
