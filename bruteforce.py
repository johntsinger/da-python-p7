import csv
from itertools import combinations as itertools_combinations


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


def find_best_stocks(stock_list):
    """Get and test each combination of stocks to find the best one
    
    Params : 
        - stock_list (list of tuple) : a stock list from a csv file

    Returns :
        - a tuple that contains :
            - the best stock list (tuple)
            - the best profits (float)
            - the total cost of the best stock list (float)
    """
    best_stock_list = ()
    best_profits = 0.0
    for i in range(len(stock_list) + 1):
        combinations = filter(
            lambda results: sum([elt[1] for elt in results]) < 500,
            itertools_combinations(stock_list, i)
        )
        best_stock_list, best_profits = get_best_combination(
            combinations, best_stock_list, best_profits)
    return (best_stock_list, best_profits, sum(
        [stock[1] for stock in best_stock_list]))


def get_best_combination(stock_combinations, best_stock_list, best_profits):
    """Test each stock list from a list of stock combinations
    to find the one that will generate the best profits

    Params :
        - stock_combinations (filter) : iterator of stock combinations
        - best_stock_list (tuple) : the last best stock list
        - best_profits (float) : the last best profits

    Returns :
        - a tuple that contains :
            - the best stocks list (tuple)
            - the best profits (float)
    """
    for stock_list in stock_combinations:
        profits = sum(
            [(stock[1] * stock[2]) / 100 for stock in stock_list]
        )
        if profits > best_profits:
            best_profits = profits
            best_stock_list = stock_list
    return (best_stock_list, best_profits)


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
              f' {"|" if int(stock[0].split("-")[1]) >= 10 else " |"}'
              f' {stock[1]} €'
              f' {"|" if stock[1] >= 100 else " |"}'
              f' {stock[2]} %')
    print()
    print(f'Cost : {results[2]} €')
    print()
    print(f'Profits : {results[1]} €')


def main():
    stocks = read_csv('stocks')
    results = find_best_stocks(stocks)
    display_rersults(results)


if __name__ == '__main__':
    main()
