import re

def remove_chevrons(text):
    return re.sub(r'<<.*?>>', '', text)
