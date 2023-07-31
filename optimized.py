import time
from decimal import Decimal
from tqdm import trange
from utils import parse_argument, read_csv


class Item:
    """Item model"""

    def __init__(self, name, weight, profit):
        self.name = name
        self.weight = float(weight)
        self.profit = float(profit)

    def __str__(self):
        return f'({self.name} {self.weight} {self.profit})'

    def __repr__(self):
        return str(self)


class Knapsack:
    """Knapsack class"""

    def __init__(self, items, max_weight):
        self.items = items
        self.multiplier = self.get_multiplier()
        self.max_weight = max_weight * self.multiplier
        self.number_of_values = len(self.items)

        # create list of the weights of each item multiplied by
        # a multiplier to get an integer
        self.weights = [
            int(item.weight * self.multiplier) for item in self.items
        ]
        # create a list of the profits of each item
        self.profits = [
            (Decimal(f'{item.profit}') * Decimal(f'{item.weight}')) / 100
            for item in self.items
        ]
        # initialize the array for the knapsack
        self.sack = [
            [0 for i in range(self.max_weight + 1)]
            for i in range(self.number_of_values + 1)
        ]
        self.results = []

    @property
    def total_cost(self):
        if self.results:
            return sum([Decimal(f'{item.weight}') for item in self.results])
        print("No result !")

    @property
    def best_profits(self):
        return self.sack[self.number_of_values][self.max_weight]

    def get_multiplier(self):
        """Get the multplier value to tranform weights
        into int if they are floats
        """
        data = [str(data.weight) for data in self.items]
        results = []
        for elt in data:
            try:
                if int(elt.split('.')[1]) > 0:
                    results.append(elt[::-1].find('.'))
            except IndexError:
                pass
        if results:
            multiplier = max(results)
            return int(f"1{'0' * multiplier}")
        return 1  # if no result multiply by 1 to not change result

    def populate(self):
        """Populate the knapsack"""
        for i in trange(1, self.number_of_values + 1):  # trange : tqdm range
            for w in range(1, self.max_weight + 1):
                if self.weights[i - 1] <= w:
                    self.sack[i][w] = max(
                        self.profits[i - 1]
                        + self.sack[i - 1][w - self.weights[i - 1]],
                        self.sack[i - 1][w])
                else:
                    self.sack[i][w] = self.sack[i - 1][w]

    def reconstruct(self):
        """Reconstruct items from the knapsack"""
        number_of_values = self.number_of_values
        max_weight = self.max_weight
        while max_weight >= 0 and number_of_values >= 0:
            try:
                if self.sack[number_of_values][max_weight] == (
                        self.sack[number_of_values - 1]
                        [max_weight - self.weights[number_of_values - 1]]
                        + self.profits[number_of_values - 1]):
                    self.results.append(self.items[number_of_values - 1])
                    max_weight -= self.weights[number_of_values - 1]
            except IndexError:
                pass
            number_of_values -= 1

    def display_results(self):
        """Better display for results"""
        print()
        print('Stocks to buy :')
        print()
        for item in self.results:
            print(f'{" " * 4}{item.name}'
                  # f' {"|" if int(stock[0].split("-")[1]) >= 10 else " |"}'
                  f' {item.weight} €'
                  # f' {"|" if stock[1] >= 100 else " |"}'
                  f' {item.profit} %')
        print()
        print(f'Cost : {self.total_cost} €')
        print()
        print(f'Profits : {self.best_profits} €')


def main():
    args = parse_argument()
    csv_data = read_csv(args.file)
    max_cost = args.invest
    items = [
        Item(data[0], data[1], data[2])
        for data in csv_data
        if float(data[1]) > 0 and float(data[2]) > 0
    ]

    # initalize knapsack
    start = time.time()
    sack = Knapsack(items, max_cost)
    init_time = time.time() - start

    # populate knapsack
    start = time.time()
    sack.populate()
    knapsack_time = time.time() - start

    # reconstruct items
    start = time.time()
    sack.reconstruct()
    reconstruct_time = time.time() - start

    sack.display_results()

    # execution time
    print()
    print('init time : ', init_time, 'sec')
    print('knapsack time : ', knapsack_time, 'sec')
    print('reconstruct time : ', reconstruct_time, 'sec')


if __name__ == '__main__':
    start = time.time()
    main()
    print('total time : ', time.time() - start, 'sec')
