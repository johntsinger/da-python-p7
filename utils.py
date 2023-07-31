import csv
import argparse


def read_csv(file_name):
    """Read csv file and return data

    Params :
        - file_name (str) : the name of the file

    Returns :
        - (list) : a list of shares
    """
    try:
        with open(f'data/{file_name}.csv', newline='') as file:
            csv_data = csv.reader(file, delimiter=',')
            next(csv_data, None)  # ignore header
            return list(csv_data)
    except FileNotFoundError:
        print("File does not exists")


def parse_argument():
    """Arguments parser"""
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