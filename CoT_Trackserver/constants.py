import logging
import os

if bool(os.environ.get('DEBUG')):
    LOG_LEVEL: int = logging.DEBUG
    LOG_FORMAT: logging.Formatter = logging.Formatter(
        ('%(asctime)s pytak %(levelname)s %(name)s.%(funcName)s:%(lineno)d - '
         '%(message)s'))
    logging.debug('pytak Debugging Enabled via DEBUG Environment Variable.')
else:
    LOG_LEVEL: int = logging.INFO
    LOG_FORMAT: logging.Formatter = logging.Formatter(
        ('%(asctime)s pytak %(levelname)s - %(message)s'))

DEFAULT_COT_IP: str = "127.0.0.1"
DEFAULT_COT_PORT: int = 8087
DEFAULT_INTERVAL: int = 60
DEFAULT_SLEEP: int = 5
accountRef: str = "USERNAME"
accountPass: str = "PASSWORD"
