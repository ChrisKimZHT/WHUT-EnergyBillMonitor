def get_history():
    with open("./history.txt", "r") as file:
        last_remain = file.read()
    return last_remain


def save_history(value):
    with open("./history.txt", "w") as file:
        file.write(value)
