"""
This script reduce a stock into matching column name/value entries.

Before hacking, please benchmark the current script with the real stock.
You should keep the duration and the RAM consumption as low as possible.
"""

import csv
import io
import sys
from zipfile import ZipFile


def _parse_zip_csv_file(filename):
    """Yield each row from a ziped CSV file coming from INSEE."""
    with ZipFile(filename) as zip_file:
        for zip_info in zip_file.infolist():
            if not zip_info.filename.endswith('.csv'):
                continue
            with zip_file.open(zip_info.filename) as csv_file:
                csvio = io.TextIOWrapper(csv_file, encoding='cp1252')
                reader = csv.DictReader(csvio, delimiter=';')
                for i, row in enumerate(reader):
                    # Not proud to pass fieldnames to each iteration.
                    # Better than a global var?
                    yield i, row, reader.fieldnames


def filter_stock(stock_in, conditions):
    """Return only matching conditions entries."""
    for i, row, fieldnames in _parse_zip_csv_file(stock_in):
        if all(row[column] == value for column, value in conditions):
            yield i, row, fieldnames


def write_stock(stock_out, filtered_stock):
    """
    Generate the new stock file with filtered entries.

    We mimick the initial stock with encoding, quotes and delimiters.
    """
    with open(stock_out, 'w', encoding='cp1252') as csv_file:
        _, first_row, fieldnames = next(filtered_stock)
        # `extrasaction` is set to `ignore` to be able to pass more keys
        # to the `writerow` method coming from the flux.
        writer = csv.DictWriter(
            csv_file, fieldnames=fieldnames, delimiter=';',
            quoting=csv.QUOTE_ALL, extrasaction='ignore')
        writer.writeheader()
        # Because we already iterate once to retrieve fieldnames.
        writer.writerow(first_row)
        # Then write the updated stock.
        for i, row, _ in filtered_stock:
            writer.writerow(row)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        BASE_USAGE = 'python stock2reduce.py stock.zip '
        print('Usages:')
        print(BASE_USAGE + 'stock-paca.csv RPET=93')
        print(BASE_USAGE + 'stock-arles.csv DEPET=13 COMET=004')
        sys.exit()
    stock_in = sys.argv[1]
    stock_out = sys.argv[2]
    conditions = [condition.split('=') for condition in sys.argv[3:]]
    filtered_stock = filter_stock(stock_in, conditions)
    write_stock(stock_out, filtered_stock)
