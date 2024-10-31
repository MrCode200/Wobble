from datetime import datetime
from logging import getLogger

from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler

from logging import DEBUG

from logging import Formatter
from logging_formatters import JsonFormatter, ColoredFormatter


def setup_logger(stream_level, stream_in_color: bool = True, log_in_json: bool = True):
    logger = getLogger('wobble.bot')
    logger.setLevel(DEBUG)

    stream_handler = StreamHandler()
    stream_handler.setLevel(stream_level)
    stream_handler.setFormatter(
        ColoredFormatter() if stream_in_color else Formatter(
            '[%(asctime)s | %(levelname)s] [%(filename)s | lineno%(lineno)d | %(funcName)s] => %(message)s'
        )
    )


    timed_rotating_file_handler = TimedRotatingFileHandler('logs/bot.log', when='midnight', interval=1, backupCount=3)
    timed_rotating_file_handler.setLevel(DEBUG)
    timed_rotating_file_handler.setFormatter(JsonFormatter() if log_in_json else Formatter(
        '[%(asctime)s | %(levelname)s] [%(filename)s | lineno%(lineno)d | %(funcName)s] => %(message)s')
    )

    logger.addHandler(stream_handler)
    logger.addHandler(timed_rotating_file_handler)


if __name__ == '__main__':
    setup_logger(DEBUG, log_in_json=True, stream_in_color=True)

    logger = getLogger('wobble.bot')
    logger.debug('Testing Logger: DEBUG')
    logger.info('Testing Logger: INFO')
    logger.warning('Testing Logger: WARNING')
    logger.error('Testing Logger: ERROR')
    logger.critical('Testing Logger: CRITICAL')

