import os
import anthropic

from clients.base_client import BaseClient

class AnthropicClient(BaseClient):
    def __init__(self, model="claude-sonnet-4-6"):
        self.model = model
        self.client = anthropic.Anthropic(
          api_key=os.environ.get("ANTHROPIC_API_KEY")
        )

    def fetch(self, system_prompt, input_messages):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            temperature=0,
            system=system_prompt,
            messages=input_messages
        )
        message = {
            "role": "assistant",
            "content": response.content[0].text,
        }
        return message


