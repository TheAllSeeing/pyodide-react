import re

def to_camel_case(snake_case: str) -> str:
    words = snake_case.split('_')
    return words[0] + ''.join(word.title() for word in words[1:])

def to_snake_case(camel_case: str) -> str:
    return '_'.join(word.title() for word in re.split('(?=[A-Z])'))