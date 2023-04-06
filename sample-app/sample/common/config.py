from pydantic import BaseModel, BaseSettings

_SETTINGS = None


class SampleSettings(BaseSettings):

    db_driver: str = "sql"
    db_name: str = None
    db_host: str = "127.0.0.1"
    db_port: int = 5432

    # log_level
    log_level: str = "DEBUG"

    # auth settings
    enable_api_key_validation: bool = True

    # SQLITE URL
    sqlite_url: str = "sqlite:///./sample.sqlite"


def override_settings(**setting_kwargs):
    global _SETTINGS
    _SETTINGS = SampleSettings(**setting_kwargs)


def get_settings():
    global _SETTINGS
    if not _SETTINGS:
        _SETTINGS = SampleSettings()
    return _SETTINGS


class LogConfig(BaseModel):
    """Logging configuration to be set for the app"""

    LOGGER_NAME: str = "sampleapp"
    LOG_FORMAT: str = "%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s"
    LOG_LEVEL: str = get_settings().log_level

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "class": "logging.Formatter",
            "format": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s %(levelname)s %(client_addr)s "%(request_line)s" %(status_code)s',
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    }
    loggers = {
        "sample": {"handlers": ["default"], "level": LOG_LEVEL},
        "uvicorn": {"handlers": ["default"], "level": LOG_LEVEL},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    }
