import json
from random import choice, choices
from json import encoder


def get_extra(shells: int) -> int:
    if shells == 2:
        return 0
    elif shells in [i for i in range(3, 9, 2)]:
        return 1
    else:
        return choice([0, 1])


def generate(max_shells: int) -> dict:
    blanks: int = (max_shells // 2) + get_extra(max_shells)
    lives: int = max_shells - blanks
    return {"shells": max_shells, "blanks": blanks, "lives": lives}


result: dict = {
    'general': generate((choice(range(2, 9)))),
    'extra': choice([
        {'shells': 3, 'blanks': 2, 'lives': 1},
        {'shells': 3, 'blanks': 1, 'lives': 2}
    ]),
    'game': {"lives": choice(range(2, 6)), "cards": choices([1, 2, 3, 4], [30, 30, 20, 20])[0]}
}

print(json.dumps(result))
