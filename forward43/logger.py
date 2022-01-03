import time
import logging


logging.basicConfig(
    format   = '[%(asctime)s] %(levelname)-8s %(message)s',
    filename = f'./logs/forward43-{int(time.time())}.log'
)

logger  = logging.getLogger('forward43')
logger.setLevel(logging.INFO)
