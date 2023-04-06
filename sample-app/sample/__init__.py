from logging.config import dictConfig

from sample.common.config import LogConfig

# setup logging and before importing the app
log_config = dictConfig(LogConfig().dict())
