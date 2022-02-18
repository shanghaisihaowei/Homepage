import random


def get_code():
    code = ''
    for i in range(6):
        code += str(random.randint(0, 9))
    return code
