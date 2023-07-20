import csv
import time
import argparse


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
            return [
                (data[0], float(data[1]), float(data[2]))
                for data in csv_data
                if float(data[1]) > 0 and float(data[2]) > 0
            ]
    except FileNotFoundError:
        print("File does not exists")


def knap_sack_2D(max_weight, weights, values, number_of_values):
    sack = [
        [0 for i in range(max_weight + 1)]
        for i in range(number_of_values + 1)
    ]
    for i in range(number_of_values + 1):
        for w in range(max_weight + 1):
            if i == 0 or w == 0:
                sack[i][w] = 0
            elif weights[i - 1] <= w:
                #print(i-1, w, w-weights[i-1], weights[i-1])
                sack[i][w] = max(
                    values[i - 1] + sack[i - 1][w - weights[i - 1]],
                    sack[i - 1][w]
                )
            else:
                sack[i][w] = sack[i - 1][w]

    return sack, sack[number_of_values][max_weight]


def reconstruct_2D(items, sack, best_profits, max_weight, weights, values,
                   number_of_values):
    results = []
    while max_weight >= 0 and number_of_values >= 0:
        try:
            if sack[number_of_values][max_weight] == (
                    sack[number_of_values - 1]
                    [max_weight - weights[number_of_values - 1]]
                    + values[number_of_values - 1]):
                results.append(items[number_of_values - 1])
                max_weight -= weights[number_of_values - 1]
        except IndexError:
            pass
        number_of_values -= 1
    return (results, best_profits, sum([shares[1] for shares in results]))


def knap_sac_1D(items, max_weight, weights, values, number_of_values):
    sack = [0 for i in range(max_weight + 1)]
    for i in range(1, number_of_values + 1):
        for w in range(max_weight, 0, -1):
            if weights[i - 1] <= w:
                sack[w] = max(
                    sack[w], sack[w - weights[i - 1]] + values[i - 1])

    # reconstruct result from knapsack
    best_profits = sack[max_weight]
    results = []
    while max_weight >= 0 and number_of_values >= 0:
        try:
            if sack[max_weight] == (
                    sack[max_weight - weights[number_of_values - 1]]
                    + values[number_of_values - 1]):
                results.append(items[number_of_values - 1])
                max_weight -= weights[number_of_values - 1]
                number_of_values = len(weights)  # reset number of items
        except IndexError:
            pass
        number_of_values -= 1
    #results.sort(key=lambda x: int(x[0].split('-')[1]), reverse=True)
    return (results, best_profits, sum([shares[1] for shares in results]))


def display_rersults(results):
    """Better display for results

    Params :
        - results (tuple) : the resutlts
    """
    print()
    print('Stocks to buy :')
    print()
    for stock in results[0]:
        print(f'{" " * 4}{stock[0]}'
              #f' {"|" if int(stock[0].split("-")[1]) >= 10 else " |"}'
              f' {stock[1]} €'
              #f' {"|" if stock[1] >= 100 else " |"}'
              f' {stock[2]} %')
    print()
    print(f'Cost : {results[2]} €')
    print()
    print(f'Profits : {results[1]} €')


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        default='stocks',
        help="The name of the file to be opened"
    )
    parser.add_argument(
        "-i",
        "--invest",
        default=500,
        type=int,
        help="The maximum investment")
    return parser.parse_args()


def main_2D():
    args = parse_argument()
    stock_list = read_csv(args.file)
    max_cost = args.invest * 100
    costs = [int(stock[1] * 100) for stock in stock_list]
    profits = [(stock[1] * stock[2]) / 100 for stock in stock_list]
    number_of_item = len(profits)
    args = {'max_weight': max_cost,
            'weights': costs,
            'values': profits,
            'number_of_values': number_of_item}
    sack, best_profits = knap_sack_2D(**args)
    results_2D = reconstruct_2D(stock_list, sack, best_profits, **args)
    display_rersults(results_2D)


def main_1D():
    args = parse_argument()
    stock_list = read_csv(args.file)
    max_cost = args.invest * 100
    costs = [int(stock[1] * 100) for stock in stock_list]
    profits = [(stock[1] * stock[2]) / 100 for stock in stock_list]
    number_of_item = len(profits)
    args = {'max_weight': max_cost,
            'weights': costs,
            'values': profits,
            'number_of_values': number_of_item}
    results_1D = knap_sac_1D(stock_list, **args)
    display_rersults(results_1D)


if __name__ == '__main__':
    start = time.time()
    main_2D()
    print('2D : ', time.time() - start, 'sec')

    start = time.time()
    main_1D()
    print('1D : ', time.time() - start, 'sec')
