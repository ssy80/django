def print_numbers():
    with open("numbers.txt", "r") as f:
        content = f.read()

    for number in content.strip().split(","):
        print(number)


if __name__ == "__main__":
    print_numbers()
