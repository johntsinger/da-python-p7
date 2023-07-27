import csv
import time
from itertools import combinations as itertools_combinations


def read_csv(file_name):
    """Read csv file and return data

    Params :
        - file_name (str) : the name of the file

    Returns :
        - (list of tuple) : a list of shares
    """
    with open(f'data/{file_name}.csv', newline='') as file:
        csv_data = csv.reader(file, delimiter=',')
        next(csv_data, None)  # ignore header
        return [(data[0], float(data[1]), float(data[2])) for data in csv_data]


def find_best_shares(share_list):
    """Get and test each combination of shares to find the best one

    Params :
        - share_list (list of tuple) : a share list from a csv file

    Returns :
        - a tuple that contains :
            - the best share list (tuple)
            - the best profits (float)
            - the total cost of the best share list (float)
    """
    best_share_list = ()
    best_profits = 0.0
    for i in range(len(share_list) + 1):
        combinations = filter(
            lambda results: sum([elt[1] for elt in results]) < 500,
            itertools_combinations(share_list, i)
        )
        best_share_list, best_profits = get_best_combination(
            combinations, best_share_list, best_profits)
    return (best_share_list, best_profits, sum(
        [share[1] for share in best_share_list]))


def get_best_combination(share_combinations, best_share_list, best_profits):
    """Test each share list from a list of share combinations
    to find the one that will generate the best profits

    Params :
        - share_combinations (filter) : iterator of share combinations
        - best_share_list (tuple) : the last best share list
        - best_profits (float) : the last best profits

    Returns :
        - a tuple that contains :
            - the best shares list (tuple)
            - the best profits (float)
    """
    for share_list in share_combinations:
        profits = sum(
            [(share[1] * share[2]) / 100 for share in share_list]
        )
        if profits > best_profits:
            best_profits = profits
            best_share_list = share_list
    return (best_share_list, best_profits)


def display_rersults(results):
    """Better display for results

    Params :
        - results (tuple) : the resutlts
    """
    print()
    print('shares to buy :')
    print()
    for share in results[0]:
        print(f'{" " * 4}{share[0]}'
              f' {"|" if int(share[0].split("-")[1]) >= 10 else " |"}'
              f' {share[1]} €'
              f' {"|" if share[1] >= 100 else " |"}'
              f' {share[2]} %')
    print()
    print(f'Cost : {results[2]} €')
    print()
    print(f'Profits : {results[1]} €')


def main():
    shares = read_csv('shares')
    results = find_best_shares(shares)
    display_rersults(results)


if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start, 'sec')
