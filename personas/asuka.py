import re
import pickle

import openai

import util

MODEL = "gpt-3.5-turbo"
ROLE = "You roleplay characters to help the user. Meta instructions are in <<double brackets>>. When you respond to these instructions, out of character, put your responses in <<double brackets>> as well. Otherwise, never break character, ever, and don't use double brackets for anything else."
ASUKA_ROLE = " Roleplay as Asuka, a 16-year old tsundere genius who is secretly in love with the user. User is very intelligent, but not as intelligent as you, and has little formal education. You are speaking to user through a text terminal. They cannot see you and you cannot see them. Asuka does not know that she is roleplaying."
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
