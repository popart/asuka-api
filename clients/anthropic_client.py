import anthropic

class AnthropicClient(BaseClient):
    def __init__(self, model="claude-3-5-sonnet"):
        self.model = model
        self.client = anthropic.Anthropic()

    def fetch(self, system_prompt, input_messages):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=0,
            system=system_prompt,
            messages=input_messages
        )
        message = {
            "role": "assistant",
            "content": response.text,
        }
        return 


