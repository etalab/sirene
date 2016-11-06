import json
import logging
from collections import defaultdict

import redis  # Do not forget to launch your `redis-server`.

from .utils import generate_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Using defaultdicts instead of storing it directly into Redis
# reduces the load time by half.
correspondences = defaultdict(dict)
correspondences_cursor = defaultdict(int)

db = redis.StrictRedis(
    host='localhost', port=6379, db=0,
    decode_responses=True  # Otherwise bytes are returned for dicts.
)
try:
    db.ping()  # Connexion is only verified on first query.
    logger.info('👌 Connected to Redis')
except redis.exceptions.BusyLoadingError:
    logger.critical('''⏱
        Your redis-server is still loading!
        Keep calm & tell you neighbor you're doing Big Data.
    ''')
    exit()
except redis.exceptions.ConnectionError:
    logger.critical('''🙅
        Your redis-server is not launched!
        Make sure it runs on localhost:6379 (defaults).
    ''')
    exit()


def has_siret(siret):
    """Checks the existence of the `siret` key."""
    return db.exists(siret)


def retrieve_siret(siret):
    """Get informations related to that `siret` from Redis."""
    return db.hgetall(siret)


def retrieve_sirets(column_name, column_value, offset=0, limit=100):
    """Return a list of `siret` codes corresponding to the exact score."""
    score = generate_score(column_name, column_value)
    return db.zrangebyscore(column_name, score, score, offset, limit)


def decode_siret(siret_data, columns):
    """
    Load the JSON stored for each modification date of a siret.

    The result of `retrieve_siret` can be passed to it directly.
    """
    return {
        datemaj: {
            k: v for k, v in json.loads(json_data).items() if k in columns
        } for datemaj, json_data in siret_data.items()
    }


def upsert_siret(siret, data, columns, check_existence):
    """
    Filter then store the `data` dict with the `siret` key in Redis.

    The ability to avoid existence checking through `check_existence`
    exists to improve performances on stock load.
    """
    data = {
        data['DATEMAJ']: json.dumps({
            # Only keep keys from columns for better performances.
            k: v for k, v in data.items() if k in columns
        })
    }
    if check_existence and has_siret(siret):
        # TODO: find a way to update without fetching/deleting/recreating?
        siret_data = retrieve_siret(siret)
        data.update(siret_data)
        db.delete(siret)
    db.hmset(siret, data)


def save_company(siret, data, columns, indexed_columns, check_existence=True):
    """Create a new indexed entry for a given `siret`."""
    compute_score(siret, data, indexed_columns)
    upsert_siret(siret, data, columns, check_existence)


def compute_score(siret, data, indexed_columns):
    """
    Compute a score for each column, then set it for a given `siret`.

    The score must be a number so we convert the couple column name/value
    into an int via a md5.
    """
    for column_name in indexed_columns:
        score = generate_score(column_name, data[column_name])
        db.zadd(column_name, score, siret)
