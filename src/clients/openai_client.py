import uuid

from openai import OpenAI

from clients.base_client import BaseClient

class OpenAIClient(BaseClient):
    def __init__(self, model="gpt-5-mini"):
        self.model = model
        self.client = OpenAI()

    def fetch(self, system_prompt, input_messages):
        input_messages.insert(0, {"role": "system", "content": system_prompt })
        print(input_messages)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=input_messages,
            #frequency_penalty=0.5,
            #presence_penalty=0.5,
            #temperature=0.0,
            reasoning_effort="low",
            verbosity="low",
            user=str(uuid.uuid4()),
        )
        print(response)
        message = {
            "role": response.choices[0].message.role,
            "content": response.choices[0].message.content or str(response.choices[0].message.tool_calls),
        }
        return message
