from openai import OpenAI

from clients.base_client import BaseClient

class OpenAIClient(BaseClient):
    def __init__(self, model="gpt-4o"):
        self.model = model
        self.client = OpenAI()

    def fetch(self, system_prompt, input_messages):
        self.base_messages.insert(0, {"role": "system", "content": system_prompt })
        response = self.client.chat.completions.create(
            model=self.model,
            messages=input_messages,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            temperature=0.0,
            user=str(uuid.uuid4()),
        )
        message = {
            "role": response.choices[0].message.role,
            "content": response.choices[0].message.content or str(response.choices[0].message.tool_calls),
        }
        return message
