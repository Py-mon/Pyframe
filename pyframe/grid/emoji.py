from json import load

with open('emojis.json', encoding='utf-8') as f:
    EMOJIS = tuple(load(f).keys())

def is_emoji(x) -> bool:
    return x in EMOJIS
