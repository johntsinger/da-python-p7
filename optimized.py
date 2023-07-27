import csv
import time
import argparse


class Item:
    def __init__(self, name, weight, profit):
        self.name = name
        self.weight = float(weight)
        self.profit = float(profit)

    def __str__(self):
        return f'({self.name} {self.weight} {self.profit})'

    def __repr__(self):
        return str(self)


class Knapsack:
    def __init__(self, items, max_weight, multiplier):
        start = time.time()
        self.items = items
        self.max_weight = max_weight * multiplier
        self.number_of_values = len(self.items)
        self.weights = [
            int(item.weight * multiplier) for item in self.items
        ]
        self.profits = [
            (item.profit * item.weight) / 100 for item in self.items
        ]
        self.sack = [
            [0 for i in range(self.max_weight + 1)]
            for i in range(self.number_of_values + 1)
        ]
        self.results = []
        self._total_cost = 0
        print('init time : ', time.time() - start, 'sec')

        start = time.time()
        # populate sack
        self.populate()
        print('knapsack time : ', time.time() - start, 'sec')

        start = time.time()
        # reconstruct items
        self.reconstruct()
        print('reconstruct time : ', time.time() - start, 'sec')

    @property
    def total_cost(self):
        if self.results:
            return sum([item.weight for item in self.results])
        print("No result !")

    @property
    def best_profits(self):
        return self.sack[self.number_of_values][self.max_weight]

    def populate(self):
        for i in range(self.number_of_values + 1):
            for w in range(self.max_weight + 1):
                if i == 0 or w == 0:
                    self.sack[i][w] = 0
                elif self.weights[i - 1] <= w:
                    self.sack[i][w] = max(
                        self.profits[i - 1]
                        + self.sack[i - 1][w - self.weights[i - 1]],
                        self.sack[i - 1][w])
                else:
                    self.sack[i][w] = self.sack[i - 1][w]

    def reconstruct(self):
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
        """Better display for results

        Params :
            - results (tuple) : the resutlts
        """
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


def read_csv(file_name):
    """Read csv file and return data

    Params :
        - file_name (str) : the name of the file

    Returns :
        - (list of tuple) : a list of stocks
    """
    try:
        with open(f'data/{file_name}.csv', newline='') as file:
            csv_data = csv.reader(file, delimiter=',')
            next(csv_data, None)  # ignore header
            return list(csv_data)
    except FileNotFoundError:
        print("File does not exists")


def get_multiplier(csv_data):
    data = [data[1] for data in csv_data]
    results = []
    for elt in data:
        try:
            if int(elt.split('.')[1]) > 0:
                results.append(elt[::-1].find('.'))
        except IndexError:
            results.append(0)
    multiplier = max(results)
    return int(f"1{'0' * multiplier}")


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        default='shares',
        help="The name of the file to be opened"
    )
    parser.add_argument(
        "-i",
        "--invest",
        default=500,
        type=int,
        help="The maximum investment")
    return parser.parse_args()


def main():
    args = parse_argument()
    csv_data = read_csv(args.file)
    multiplier = get_multiplier(csv_data)
    max_cost = args.invest
    items = [
        Item(data[0], data[1], data[2])
        for data in csv_data
        if float(data[1]) > 0 and float(data[2]) > 0
    ]
    sack = Knapsack(items, max_cost, multiplier)
    sack.display_results()


if __name__ == '__main__':
    start = time.time()
    main()
    print('total time : ', time.time() - start, 'sec')
