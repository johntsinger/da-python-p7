import time
from itertools import combinations as itertools_combinations
from tqdm import trange
from utils import parse_argument, read_csv


def find_best_shares(share_list, max_cost):
    """Get and test each combination of shares to find the best one

    Params :
        - share_list (list of tuple) : a share list from a csv file

    Returns :
        - a tuple that contains :
            - the best shares list (tuple)
            - the best profits (float)
            - the total cost of the best share list (float)
    """
    best_shares_list = ()
    best_profits = 0.0
    for i in trange(1, len(share_list) + 1):
        combinations = filter(
            lambda results: sum([elt[1] for elt in results]) < max_cost,
            itertools_combinations(share_list, i)
        )
        best_shares_list, best_profits = get_best_combination(
            combinations, best_shares_list, best_profits)
    return (best_shares_list, best_profits, sum(
        [share[1] for share in best_shares_list]))


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
              f' {share[1]} €'
              f' {share[2]} %')
    print()
    print(f'Cost : {results[2]} €')
    print()
    print(f'Profits : {results[1]} €')


def main():
    args = parse_argument()
<<<<<<< HEAD
    if args.file in ('dataset1', 'dataset2'):
        print()
        print(f"WARNING : The file {args.file} contains too many data "
              "to be used with brute force algorithm ! "
              "This can saturate your RAM !"
              "\nPlease use shares file instead")
        exit()
=======
>>>>>>> f65946fa058cc68a15c3d757cc14f2ad8a1287e7
    csv_data = read_csv(args.file)
    max_cost = args.invest
    shares = [
        (share[0], float(share[1]), float(share[2])) for share in csv_data
    ]
    results = find_best_shares(shares, max_cost)
    display_rersults(results)


if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start, 'sec')
