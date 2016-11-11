import logging

from jsondiff import diff
from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import ServerError

from .database import decode_siret, retrieve_siret, retrieve_sirets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def dict_to_csv(row, column_names, separator=';'):
    """Turn a `row` of dicts into one or many CSV row(s)."""
    lines = []
    for datemaj, data in sorted(row.items()):
        line = separator.join(
            column_name in data and data[column_name] or ''
            for column_name in column_names
        )
        lines.append(line)
    return '\n'.join(lines)


def format_response(rows, format, column_names):
    """Given a `format`, serialize and return the appropriated data."""
    if format == 'json':
        return json(rows)
    elif format == 'csv':
        headers = ';'.join(column_names) + '\n'
        rows = [dict_to_csv(row, column_names) for row in rows]
        return text(headers + '\n'.join(rows))


app = Sanic(__name__)


@app.route('/diff/<siret>')
async def diff_view(request, siret):
    """Retrieve the diff of data for a given `siret`."""
    start_date = request.args.get('start-date')
    end_date = request.args.get('end-date')
    logger.info('🙇 Requesting diff for {0} from {1} to {2}'.format(
                siret, start_date, end_date))
    data = decode_siret(retrieve_siret(siret), app.config.columns)
    try:
        result = diff(data[start_date], data[end_date], syntax='symmetric')
    except KeyError:
        msg = '😢 Invalid dates {0}/{1}'.format(start_date, end_date)
        raise ServerError(msg)
    return json(result)


@app.route('/<name>/<value>')
async def info_view(request, name, value):
    """Retrieve JSON or CSV encoded items give the name/value filter."""
    limit = int(request.args.get('limit', 3))
    offset = int(request.args.get('offset', 0))
    format = request.args.get('format', 'json')
    logger.info('🙇 Requesting {0} (offset={1}) items in {2}'.format(
                limit, offset, format))
    columns = request.args.get('columns')
    column_names = columns and columns.split(',') or app.config.columns
    sirets = retrieve_sirets(name, value, offset=offset, limit=limit)
    if not sirets:
        raise ServerError('😢 No entry found for {0}/{1}'.format(name, value))
    logger.info('🐿 Retrieving {0} results for the {1}/{2} couple'.format(
                len(sirets), name, value))
    logger.info('🍫 Returning {0} results in {1}'.format(len(sirets), format))
    rows = [decode_siret(retrieve_siret(siret), column_names)
            for siret in sirets]
    return format_response(rows, format, column_names)
