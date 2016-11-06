from argparse import ArgumentParser

from .constants import (
    DEFAULT_COLUMNS, DEFAULT_EXCLUDED_COLUMNS, DEFAULT_UPDATE_COLUMNS
)
from .loaders import load_stock, load_updates
from .server import app

if __name__ == '__main__':
    parser = ArgumentParser(prog='ulysse')
    parser.add_argument(
        '--lines', dest='lines', type=int, default=1000,
        help='number of lines you want to process (default=1000)')
    parser.add_argument(
        '--filename', dest='filename',
        help='path of your source CSV file for loading data')
    parser.add_argument(
        '--folder', dest='folder',
        help='path of your folder containing data updates')
    parser.add_argument(
        '--columns', dest='columns', nargs='+',
        default=DEFAULT_COLUMNS,
        help=('columns you want to work on, '
              'this is recommended to keep at least `SIREN`'))
    parser.add_argument(
        '--update-columns', dest='update_columns', nargs='+',
        default=DEFAULT_UPDATE_COLUMNS,
        help=('update columns you want to work on, '
              'this is recommended to keep at least `VMAJ`?'))
    parser.add_argument(
        '--excluded', dest='excluded', nargs='+',
        default=DEFAULT_EXCLUDED_COLUMNS,
        help='columns excluded from indexation (free text for instance)')
    parser.add_argument(
        '--debug', dest='debug', action='store_true',
        help='only in use with the serve command for server debugger')
    parser.add_argument(
        'command', help='either `load_stock`, `load_updates` or `serve`')
    args = parser.parse_args()

    if args.command.startswith('load'):
        indexed_columns = [
            column_name for column_name in args.columns
            if not any(column_name.endswith(suffix)
                       for suffix in args.excluded)
        ]
        if args.command == 'load_stock':
            load_stock(args.filename, nb_of_lines=args.lines,
                       columns=args.columns, indexed_columns=indexed_columns)
        elif args.command == 'load_updates':
            load_updates(args.folder, update_columns=args.update_columns,
                         columns=args.columns, indexed_columns=indexed_columns)
    elif args.command == 'serve':
        app.config.columns = args.columns  # TODO: is that The Right Way©?
        app.run(host='0.0.0.0', port=8000, debug=args.debug)
