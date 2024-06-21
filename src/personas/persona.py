import sys
import logging
import uuid

from openai import OpenAI

client = OpenAI()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEFAULT_SYSTEM_PROMPT = "User will give you a role and you will respond in that role. Respond directly in character. Do not provide narrative."
DEFAULT_COMPLIANCE = "[Understand. Please give me my role, and then I will respond in that role going forward.]"

class Persona:

    def __init__(
            self,
            client,
            system_prompt=DEFAULT_SYSTEM_PROMPT,
            compliance=DEFAULT_COMPLIANCE,
            role=None,
            examples=None):
        self.client = client
        self.system_prompt = system_prompt
        self.base_messages = []

        if compliance:
            self.base_messages.append({"role": "assistant", "content": compliance })

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

        messages = system_messages + chat_messages[-10:]
            
        input_messages = self.base_messages.copy() + messages

        message = self.client.fetch(
            system_prompt=self.system_prompt,
            system_messages=system_messages,
            input_messages=input_messages
        )
        return message
