"""
This script converts a stock + flux into a new updated stock.

Before hacking, please benchmark the current script with the real stock.
You should keep the duration and the RAM consumption as low as possible.
"""

import csv
import io
import os
import sys
from zipfile import ZipFile


def _parse_zip_csv_file(filename):
    """Yield each row from a ziped CSV file coming from INSEE."""
    base_name, ext = os.path.splitext(os.path.basename(filename))
    with ZipFile(filename) as zip_file:
        with zip_file.open(base_name + '.csv') as csv_file:
            csvio = io.TextIOWrapper(csv_file, encoding='cp1252')
            reader = csv.DictReader(csvio, delimiter=';')
            for i, row in enumerate(reader):
                # Not proud to pass fieldnames to each iteration.
                # Better than a global var?
                yield i, row, reader.fieldnames


def parse_fluxs(sources):
    """For each line from sources, create a dict with SIRET as key."""
    return {
        # SIREN + NIC = SIRET.
        row['SIREN'] + row['NIC']: row
        for source in sources
        for i, row, _ in _parse_zip_csv_file(source)
    }


def filter_stock(stock_in, modifications):
    """Return modified entries and not deleted ones."""
    for i, row, fieldnames in _parse_zip_csv_file(stock_in):
        entry = modifications.get(row['SIREN'] + row['NIC'], row)
        is_deleted = 'VMAJ' in entry and entry['VMAJ'] == 'E'
        if not is_deleted:
            yield i, entry, fieldnames


def write_stock(stock_out, filtered_stock, modifications):
    """
    Generate the new stock file with modified and created entries.

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
        for i, row, _ in filtered_stock:
            writer.writerow(row)
        # Finally, append creations.
        for siret, row in modifications.items():
            is_created = row['VMAJ'] == 'C'
            if is_created:
                writer.writerow(row)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        BASE_USAGE = 'python flux2stock.py stock-t.zip '
        print('Usages:')
        print(BASE_USAGE + 'stock-t+1.csv flux-t+1.zip')
        print(BASE_USAGE + 'stock-t+2.csv flux-t+1.zip flux-t+2.zip')
    stock_in = sys.argv[1]
    stock_out = sys.argv[2]
    fluxs_zip = sys.argv[3:]
    modifications = parse_fluxs(fluxs_zip)
    filtered_stock = filter_stock(stock_in, modifications)
    write_stock(stock_out, filtered_stock, modifications)
