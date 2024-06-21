import sys
import logging
import uuid

from openai import OpenAI

client = OpenAI()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#MODEL = "gpt-3.5-turbo"
#MODEL = "gpt-4"
#MODEL = "gpt-4-1106-preview" # gpt-4 turbo
#MODEL = "gpt-4-turbo" # gpt-4 turbo
MODEL = "gpt-4o" # gpt-4 turbo

BASE_ROLE = "User will give you a role and you will respond in that role. Respond directly in character. Do not provide narrative."
BASE_COMPLIANCE = "[Understand. Please give me my role, and then I will respond in that role going forward.]"


class Persona:

    def __init__(self, name=None, role=None, compliance=None, examples=None):
        self.base_messages = []
        self.base_messages.append({"role": "system", "content": BASE_ROLE })
        self.base_messages.append({"role": "assistant", "content": BASE_COMPLIANCE })

        if role:
            self.base_messages.append({"role": "user", "content": role })

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
            temperature=0.0,
            user=str(uuid.uuid4()),
        )

        logger.info(response)

        message = {
            "content": response.choices[0].message.content or str(response.choices[0].message.tool_calls),
            "role": response.choices[0].message.role,
        }

        logger.info(f"openai response: {message}")

        return message

model_persona = Persona()
