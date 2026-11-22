import random

from beverages import HotBeverage, Coffee, Tea, Chocolate, Cappuccino


class CoffeeMachine:
    MAX_SERVES = 10

    class EmptyCup(HotBeverage):
        price = 0.90
        name = "empty cup"

        def description(self):
            return "An empty cup?! Gimme my money back!"

    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def __init__(self):
        self.served = 0

    def repair(self):
        self.served = 0

    def serve(self, beverage):
        if self.served >= self.MAX_SERVES:
            raise self.BrokenMachineException()
        self.served += 1
        if random.randint(0, 1):
            return beverage()
        return self.EmptyCup()


def main():
    machine = CoffeeMachine()
    drinks = (HotBeverage, Coffee, Tea, Chocolate, Cappuccino)

    for _ in range(2):
        try:
            while True:
                print(machine.serve(random.choice(drinks)))
                print()
        except CoffeeMachine.BrokenMachineException as e:
            print(e)
            print()
        machine.repair()


if __name__ == "__main__":
    main()
