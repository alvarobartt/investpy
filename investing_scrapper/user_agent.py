import random


def get_random():
    file = 'data/user-agent-list.txt'

    with open(file, 'r') as f:
        lines = f.readlines()
        return str(random.choice(lines)).replace("\n", "")
