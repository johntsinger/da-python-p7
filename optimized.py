import csv
import time


def read_csv(file_name):
    """Read csv file and return data

    Params :
        - file_name (str) : the name of the file

    Returns :
        - (list of tuple) : a list of stocks
    """
    with open(f'data/{file_name}.csv', newline='') as file:
        csv_data = csv.reader(file, delimiter=',')
        next(csv_data, None)  # ignore header
        return [(data[0], float(data[1]), float(data[2])) for data in csv_data]


def knap_sack_2D(max_weight, weights, items, number_of_item):
    sack = [
        [0 for i in range(max_weight + 1)] for i in range(number_of_item + 1)
    ]
    for i in range(number_of_item + 1):
        for w in range(max_weight + 1):
            if i == 0 or w == 0:
                sack[i][w] = 0
            elif weights[i-1] <= w:
                sack[i][w] = max(items[i-1][2] + sack[i-1][w-weights[i-1]],
                                 sack[i-1][w])
            else:
                sack[i][w] = sack[i-1][w]

    best_profits = sack[number_of_item][max_weight]

    results = []
    while max_weight >= 0 and number_of_item >= 0:
        if sack[number_of_item][max_weight] == sack[number_of_item - 1][max_weight - weights[number_of_item - 1]] + items[number_of_item - 1][2]:
            results.append(items[number_of_item - 1])
            max_weight -= weights[number_of_item - 1]
        number_of_item -= 1
    return best_profits, results


def knap_sac_1D(max_weight, weights, items, number_of_item):
    sack = [0 for i in range(max_weight + 1)]
    for i in range(1, number_of_item + 1):
        for w in range(max_weight, 0, -1):
            if weights[i-1] <= w:
                sack[w] = max(sack[w], sack[w-weights[i-1]] + items[i-1][2])
    best_profits = sack[max_weight]
    results = []
    while max_weight >= 0 and number_of_item >= 0:
        if sack[max_weight] == sack[max_weight - weights[number_of_item - 1]] + items[number_of_item - 1][2]:
            results.append(items[number_of_item-1])
            max_weight -= weights[number_of_item-1]
            number_of_item = len(weights)  # reset number of items
        number_of_item -= 1
    # results.sort(key=lambda x: int(x[0].split('-')[1]), reverse=True)  # can be removed
    return best_profits, results


def main_2D():
    stock_list = read_csv('stocks')
    stock_list = [(stock[0], stock[1], (stock[1] * stock[2]) / 100)
                  for stock in stock_list]
    max_weight = 500
    number_of_item = len(stock_list)
    weights = [int(stock[1]) for stock in stock_list]
    results_2D = knap_sack_2D(max_weight, weights, stock_list, number_of_item)
    print(results_2D)


def main_1D():
    stock_list = read_csv('stocks')
    stock_list = [(stock[0], stock[1], (stock[1] * stock[2]) / 100) for stock in stock_list]
    max_weight = 500
    number_of_item = len(stock_list)
    weights = [int(stock[1]) for stock in stock_list]
    results_1D = knap_sac_1D(max_weight, weights, stock_list, number_of_item)
    print(results_1D)


if __name__ == '__main__':
    start = time.time()
    main_2D()
    print('2D : ', time.time() - start, 'sec')

    start = time.time()
    main_1D()
    print('1D : ', time.time() - start, 'sec')
