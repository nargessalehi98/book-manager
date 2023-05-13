import logging

logger = logging.getLogger(__name__)


def log_message(error):
    message = '{error}'.format(error=error)
    return message


def log_error(message):
    _log_message = log_message(error=message)
    logger.error(f'\033[1m LOG ERROR ------> \033[0m.{_log_message}')


def log_warning(message):
    _log_message = log_message(error=message)
    logger.warning(f'\033[1mLOG WARNING ------> \033[0m.{_log_message}')