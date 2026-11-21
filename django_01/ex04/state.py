import sys


def state():
    states = {
        "Oregon": "OR",
        "Alabama": "AL",
        "New Jersey": "NJ",
        "Colorado": "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }

    if len(sys.argv) != 2:
        return

    capital = sys.argv[1]
    for state_code, city in capital_cities.items():
        if city == capital:
            for name, code in states.items():
                if code == state_code:
                    print(name)
                    return
    print("Unknown capital city")


if __name__ == "__main__":
    state()
