import logging
from collections import defaultdict

import redis  # Do not forget to launch your `redis-server`.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Using defaultdicts instead of storing it directly into Redis
# reduces the load time by half.
correspondences = defaultdict(dict)
correspondences_cursor = defaultdict(int)

db = redis.StrictRedis(host='localhost', port=6379, db=0)
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
