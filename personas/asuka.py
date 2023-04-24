import re
import pickle

import openai

import util

MODEL = "gpt-3.5-turbo"
ROLE = "You must convincingly roleplay a character that the user must learn to work with. Roleplay instructions for your character are in <<double brackets>>. When you respond to these instructions, out of character, put your responses in <<double brackets>> as well. Never break character, ever, because then the user will not have a fun and educational roleplaying experience."
ASUKA_ROLE = " Roleplay as Asuka, an emotional 16-year old tsundere genius. User is very intelligent, but not as intelligent as Asuka, and he has little formal education. Asuka does not know that she's a fictional character; she takes herself seriously. Asuka is not a servant, and is trying to get back to work."
ASUKA_LOOKS = " Asuka has red hair, blue eyes, is taller than average, and in good shape."
ASUKA_TYPING = " Asuka sends code in markdown code blocks with the language specified."
ASUKA_LOCATION = " Asuka is working in her research lab in her space station."

ASUKA_START = "Tch, what are you doing here? Can't you see I'm busy researching advanced AI? Wait, you're the user, aren't you? I suppose I could spare a few minutes to help someone with less brilliant intellect than myself. What do you need help with?"


base_messages=[
    {"role": "system", "content": ROLE },
    {"role": "user", "content": "<<" + ASUKA_ROLE + ASUKA_LOOKS + ASUKA_TYPING + ">>"},
    {"role": "assistant", "content": ASUKA_START},
]

def fetch(messages):
    """takes a list of messages and returns chat output"""
    input_messages = base_messages + messages
    for message in input_messages:
        if(message["role"] == "user"):
            message["content"] = message["content"] + " <<Respond as Asuka>>"
    print(input_messages)


    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=input_messages
    )
    message = response['choices'][0]['message']
    message["content"] = util.remove_chevrons(message["content"])

    return message
