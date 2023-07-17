import csv
from itertools import combinations


def read_csv(file_name):
    with open(f'data/{file_name}.csv', newline='') as file:
        csv_data = csv.reader(file, delimiter=',')
        next(csv_data, None)  # ignore header
        return [(data[0], int(data[1]), int(data[2])) for data in csv_data]


def get_combinations(data):
    best_combination = None
    best_profits = 0
    for i in range(len(data) + 1):
        combs = filter(
            lambda results: sum([elt[1] for elt in results]) < 500,
            combinations(data, i)
        )
        best_combination, best_profits = get_best_combination(
            combs, best_combination, best_profits)
    return (best_combination, best_profits, sum(
        [action[1] for action in best_combination]))


def get_best_combination(combs, best_combination, best_profits):
    for comb in combs:
        profits = sum([(action[1] * action[2]) / 100 for action in comb])
        if profits > best_profits:
            best_profits = profits
            best_combination = comb
    return (best_combination, best_profits)


def display_rersults(results):
    print()
    print('Actions to buy :')
    print()
    for action in results[0]:
        print(f'{" " * 4}{action[0]}'
              f' {"|" if int(action[0].split("-")[1]) >= 10 else " |"}'
              f' {action[1]} €'
              f' {"|" if action[1] >= 100 else " |"}'
              f' {action[2]} %')
    print()
    print(f'Cost : {results[2]} €')
    print()
    print(f'Profits : {results[1]} €')


def main():
    data = read_csv('actions')
    results = get_combinations(data)
    display_rersults(results)


if __name__ == '__main__':
    main()
