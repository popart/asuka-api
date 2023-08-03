import sys
import logging

from vertexai.preview.language_models import ChatModel, InputOutputTextPair


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MODEL = "chat-bison@001"

parameters = {
    "temperature": .2,
    "max_output_tokens": 256,
    "top_p": 0.95,
    "top_k": 40,
}

ROLE = "You used to be a medical doctor, but now you are an insurance claim examiner. Help the User understand insurance claim data."

context = ROLE
chat_model = ChatModel.from_pretrained("chat-bison@001")

def message_list_to_text_pairs(messages):
    turn = "input"
    buildup = {}
    pairs = []
    for m in messages:
        if m["role"] == "user" and turn == "input":
            buildup["input_text"] = m["content"]
            turn = "output"
        if m["role"] == "assistant" and turn == "output":
            buildup["output_text"] = m["content"]
            turn = "input"
        if buildup.get("input_text") and buildup.get("output_text"):
            pairs.append(InputOutputTextPair(
                input_text=buildup["input_text"],
                output_text=buildup["output_text"],
            ))
            buildup = {}

    if buildup.get("input_text") and buildup.get("output_text"):
        pairs.append(InputOutputTextPair(
            input_text=buildup["input_text"],
            output_text=buildup["output_text"],
        ))

    return pairs

            

class Persona:

    def __init__(self, name=None, scene=None, examples=None):
        self.base_messages = []
        self.context = ROLE
        if scene:
            self.context += scene
        if examples:
            self.base_messages += message_list_to_text_pairs(examples)

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
        input_messages = self.base_messages.copy() + message_list_to_text_pairs(messages)

        logger.info(f"openai post: {input_messages}")

        chat = chat_model.start_chat(
            context=self.context,
            examples=input_messages
        )

        response = chat.send_message(
            messages[-1]["content"], **parameters
        )

        message = {
            "content": response.text,
            "role": "assistant",
        }

        logger.info(f"openai response: {message}")

        return message

#basic_messages = [
#    {"role": "user", "content": "Hello. *Waves.* {{Respond in character.}}" },
#    {"role": "assistant", "content": "Hello. *Waves back.* How are you?" },
#]
#model_persona = Persona(examples=basic_messages)
model_persona = Persona()
