import logging

from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import ServerError

from .constants import DEFAULT_COLUMNS
from .database import db
from .utils import _generate_score_key

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_sirens(column_name, column_value):
    """Return a list of `siren` codes corresponding to the match."""
    score_key = _generate_score_key(column_name, column_value)
    score = db.get(score_key)
    if not score:
        msg = '😢 No entry found for {0}/{1}, is it indexed?'.format(
            column_name, column_value)
        logger.error(msg)
        raise ServerError(msg)
    return db.zrangebyscore(column_name, score, score)


def _redis_to_dict(siren, column_names, encoding='utf-8'):
    """Turn a Redis response into a decoded dict."""
    return {
        k.decode(encoding): v.decode(encoding)
        for k, v in db.hgetall(siren).items()
        if k.decode(encoding) in column_names
    }


def _redis_to_csv(siren, column_names, encoding='utf-8', separator=';'):
    """Turn a Redis response into a CSV row."""
    data = db.hgetall(siren)
    return separator.join([
        data[str.encode(column_name)].decode(encoding)
        for column_name in column_names
    ])


def _format_response(sirens, format, column_names):
    """Given a `format`, fetch, serialize and return the appropriated data."""
    if format == 'json':
        try:
            rows = [_redis_to_dict(siren, column_names) for siren in sirens]
        except KeyError as e:
            msg = '⁉️ Retrieving a column that is not stored: {0}'.format(e)
            logger.error(msg)
            raise ServerError(msg)
        return json(rows)
    elif format == 'csv':
        headers = ';'.join(column_names) + '\n'
        try:
            rows = [_redis_to_csv(siren, column_names) for siren in sirens]
        except KeyError as e:
            msg = '⁉️ Retrieving a column that is not stored: {0}'.format(e)
            logger.error(msg)
            raise ServerError(msg)
        return text(headers + '\n'.join(rows))


app = Sanic(__name__)


@app.route('/<name>/<value>')
async def server(request, name, value):
    limit = int(request.args.get('limit', 3))
    format = request.args.get('format', 'json')
    logger.info('🙇 Requesting {0} items in {1}'.format(limit, format))
    columns = request.args.get('columns')
    column_names = columns and columns.split(',') or app.config.COLUMNS
    sirens = _get_sirens(name, value)
    logger.info('🐿 Retrieving {0} results for the {1}/{2} couple'.format(
                len(sirens), name, value))
    sirens = sirens[:limit]
    logger.info('🍫 Returning {0} results in {1}'.format(len(sirens), format))
    return _format_response(sirens, format, column_names)
