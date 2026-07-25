import random


def create_game(level):

    if level == "easy":

        a = random.randint(1, 20)
        b = random.randint(1, 20)

        op = random.choice(["+", "-"])


    elif level == "medium":

        a = random.randint(10, 70)
        b = random.randint(10, 70)

        op = random.choice(["+", "-", "*"])


    else:

        op = random.choice(["+", "-", "*", "/"])

        if op == "/":

            b = random.randint(2, 12)
            answer = random.randint(2, 12)
            a = b * answer

        else:

            a = random.randint(20, 120)
            b = random.randint(20, 120)


    if op == "+":
        answer = a + b

    elif op == "-":
        answer = a - b

    elif op == "*":
        answer = a * b

    elif op == "/":
        answer = a // b


    return {
        "question": f"{a} {op} {b}",
        "answer": answer,
        "level": level
    }


def check(game, text):

    try:

        return int(text) == game["answer"]

    except:

        return False
