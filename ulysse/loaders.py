import csv
import logging

from .database import db, correspondences, correspondences_cursor
from .utils import _generate_score_key

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_stock(filename, nb_of_lines, columns, indexed_columns):
    """Load `nb_of_lines` lines from `filename` into a Redis database."""
    logger.info('👉 Loading {0} lines from {1}'.format(nb_of_lines, filename))
    with open(filename, encoding='cp1252') as file:
        for i, data in enumerate(csv.DictReader(file, delimiter=';')):
            if i and not i % 10000:
                logger.info('💧 Already {0} lines loaded'.format(i))

            if i > nb_of_lines:
                break

            siren = data['SIREN']
            _store_column_score(siren, data, indexed_columns)
            _store_data(siren, data, columns)
    # Only store correspondences at the end to allow permanence of
    # the correspondences and make possible future fetching.
    _store_corresondences(correspondences)
    logger.info('🌊 {0} lines loaded with success'.format(nb_of_lines))


def _store_corresondences(correspondences):
    """
    Convert defaultdicts of correspondances into Redis keys/values.

    By doing this afterwards, we reduce the time of the initial load
    by half. However, we need it stored to be used by the API later.
    """
    logger.info('💦 Storing correspondences (last step!)')
    for column_name, column_value_dict in correspondences.items():
        for column_value, score_value in column_value_dict.items():
            score_key = _generate_score_key(column_name, column_value)
            db.set(score_key, score_value)


def _store_data(siren, data, columns):
    """Filter then store the `data` dict with the `siren` key in Redis."""
    db.hmset(siren, {
        # Only keep keys from columns for better performances.
        k: v for k, v in data.items() if k in columns
    })


def _store_column_score(siren, data, indexed_columns):
    """Compute a score for each column, then set it for a given `siren`."""
    # Note that it requires a score as a float,
    # hence the column counter/name conversion.
    for column_name in indexed_columns:
        value = data[column_name]
        correspondence = correspondences[column_name]
        if value not in correspondence:
            correspondence[value] = correspondences_cursor[column_name]
            correspondences_cursor[column_name] += 1
        score = correspondence[value]
        db.zadd(column_name, score, siren)
