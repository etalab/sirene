import logging
from collections import Counter

from .database import save_company
from .utils import extract_csv_filepaths, iter_over_csv_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_stock(filename, nb_of_lines, columns, indexed_columns):
    """Load `nb_of_lines` lines from `filename` into a Redis database."""
    logger.info('👉 Loading {0} lines from {1}'.format(nb_of_lines, filename))
    for i, data in iter_over_csv_file(filename):
        if i and not i % 10000:
            logger.info('💧 Already {0} lines loaded'.format(i))

        if i > nb_of_lines:
            break

        siret = data['SIREN'] + data['NIC']
        save_company(
            siret, data, columns, indexed_columns, check_existence=False)
    logger.info('🌊 {0} lines loaded with success'.format(nb_of_lines))


def load_updates(folder, update_columns, columns, indexed_columns):
    total_items = 0
    for csv_filepath in extract_csv_filepaths(folder):
        logger.info('👉 Loading data from {0}'.format(csv_filepath))
        counter = Counter({
            'creations': 0,
            'modifications': 0,
            'deletions': 0,
            'commercial': 0,
            'not_commercial': 0
        })
        for i, data in iter_over_csv_file(csv_filepath):
            if i and not i % 3000:
                logger.info('💧 Already {0} lines loaded'.format(i))

            vmaj = data['VMAJ']
            siret = data['SIREN'] + data['NIC']
            is_creation = vmaj == 'C'
            is_update_old = vmaj == 'I'
            is_update_new = vmaj == 'F'
            is_deletion = vmaj == 'E'
            is_commercial = vmaj == 'D'
            is_not_commercial = vmaj == 'O'

            if is_creation:
                counter['creations'] += 1
            elif is_update_old:
                # We remove one day from DATEMAJ to keep track of that state,
                # might be useful if company hasn't been loaded from stock.
                # TODO: really convert to a date! (or do not keep line?)
                data['DATEMAJ'] = str(int(data['DATEMAJ']) - 1)
            elif is_update_new:
                counter['modifications'] += 1
                # TODO: make sure that infos about the modif are propagated.
            elif is_deletion:
                counter['deletions'] += 1
                # TODO: make sure that infos about the deletion are propagated.
            elif is_commercial:
                counter['commercial'] += 1
            elif is_not_commercial:
                counter['not_commercial'] += 1
            else:
                raise Exception('Update not supported: "{0}"'.format(vmaj))

            save_company(siret, data, columns+update_columns, indexed_columns)

        logger.info((
            '🐣 Creations: {creations} — '
            '👥 Modifications: {modifications} — '
            '💀 Deletions: {deletions} — '
            '🤑 Commercial: {commercial} — '
            '💸 Non commercial: {not_commercial}').format(**dict(counter)))
        total_items += i
    logger.info('🌊 {0} items loaded with success'.format(total_items))
