import sys


def all_in():
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

    arg = sys.argv[1]
    if ",," in arg:
        return

    for expr in arg.split(","):
        expr = " ".join(expr.split())   # trim and collapse multiple spaces
        if not expr:
            continue

        found = False
        for state, code in states.items():
            capital = capital_cities[code]
            if expr.lower() == state.lower() or expr.lower() == capital.lower():
                print(f"{capital} is the capital of {state}")
                found = True
                break

        if not found:
            print(f"{expr} is neither a capital city nor a state")


if __name__ == "__main__":
    all_in()
