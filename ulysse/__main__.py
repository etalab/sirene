from argparse import ArgumentParser

from .constants import DEFAULT_COLUMNS, DEFAULT_EXCLUDED_COLUMNS
from .loaders import load_stock
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
        '--columns', dest='columns', nargs='+',
        default=DEFAULT_COLUMNS,
        help=('columns you want to work on, '
              'this is recommended to keep at least `SIREN`'))
    parser.add_argument(
        '--excluded', dest='excluded', nargs='+',
        default=DEFAULT_EXCLUDED_COLUMNS,
        help='columns excluded from indexation (free text for instance)')
    parser.add_argument(
        '--debug', dest='debug', action='store_true',
        help='only in use with the serve command for server debugger')
    parser.add_argument('command', help='either `load` or `serve`')
    args = parser.parse_args()

    if args.command == 'load':
        indexed_columns = [
            column_name for column_name in args.columns
            if not any(column_name.endswith(suffix)
                       for suffix in args.excluded)
        ]
        load_stock(args.filename, nb_of_lines=args.lines, columns=args.columns,
                   indexed_columns=indexed_columns)
    elif args.command == 'serve':
        app.config.columns = args.columns  # TODO: is that The Right Way©?
        app.run(host='0.0.0.0', port=8000, debug=args.debug)


'''
→ python ulysse.py load --lines 1000000
Time: about 15 minutes
Source file: 12 million lines - only 1 million loaded
Redis: "less" than 3Gb of ram during the initial load
       then 200Mb (disk) + 1Gb (ram) + 24s (initial load)

→ python ulysse.py serve --debug

→ http :8000/NIC/00056 limit==3
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 544
Content-Type: application/json; charset=utf-8
Keep-Alive: timeout=60

[
    {
        "APEN700": "4669B",
        "CATEGORIE": "PME",
        "DATEMAJ": "20110719",
        "DEFET": "2009",
        "DEPCOMEN": "80001",
        "L1_NORMALISEE": "ETABLISSEMENTS LUCIEN BIQUEZ",
        "NIC": "00056",
        "SIREN": "005420021",
        "TEFET": "11"
    },
    {
        "APEN700": "6820B",
        "CATEGORIE": "",
        "DATEMAJ": "20150902",
        "DEFET": "2015",
        "DEPCOMEN": "04070",
        "L1_NORMALISEE": "MONSIEUR PHILIPPE PLOGE",
        "NIC": "00056",
        "SIREN": "006641823",
        "TEFET": "00"
    },
    {
        "APEN700": "4312B",
        "CATEGORIE": "PME",
        "DATEMAJ": "20120120",
        "DEFET": "2014",
        "DEPCOMEN": "04209",
        "L1_NORMALISEE": "ENTREPRISE MINETTO",
        "NIC": "00056",
        "SIREN": "007350200",
        "TEFET": "01"
    }
]
Time: about 200ms

→ http :8000/NIC/00056 limit==6 format==csv columns==SIREN,L1_NORMALISEE
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 235
Content-Type: text/plain; charset=utf-8
Keep-Alive: timeout=60

SIREN;L1_NORMALISEE
005420021;ETABLISSEMENTS LUCIEN BIQUEZ
006641823;MONSIEUR PHILIPPE PLOGE
007350200;ENTREPRISE MINETTO
025550120;LAITERIE NOUVELLE DE L ARGUENON
045550647;SOCIETE DE TRANSPORTS ET DE SERVICES
055807044;LAURENT ET CIE
Time: about 200ms

TODO:

* try to load the whole file?! (x12)
* load daily updates
'''
