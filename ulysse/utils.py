import csv
import hashlib
import os


def generate_score(column_name, column_value):
    """
    Return an int from a couple name/value.

    To be a valid score for Redis, it has to be between
    -9007199254740992 and 9007199254740992.
    See: http://redis.io/commands/zadd
    """
    # TODO: check for collisions? potential performances bottleneck?
    key = (column_name + column_value).encode('utf-8')
    base = ''.join(str(ord(c)) for c in hashlib.md5(key).hexdigest())
    return int(base[:15])


def extract_csv_filepaths(folder):
    """Walk over a `folder` to yield every CSV filepaths in it."""
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith('.csv'):
                yield os.path.join(dirpath, filename)


def iter_over_csv_file(csv_filepath):
    """Open and enumerate over a CSV file located at `csv_filepath`."""
    with open(csv_filepath, encoding='cp1252') as csv_file:
        for i, data in enumerate(csv.DictReader(csv_file, delimiter=';')):
            yield i, data
