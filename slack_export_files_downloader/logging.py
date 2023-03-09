import logging
import sys

__logger_initialised = False


def get_logger():
    """ Get the logger for this package. The first time this function is
    called the logger is created, configured and returned. Subsequent calls
    just return the logger.
    
    """
    global __logger_initialised

    logger = logging.getLogger('slack_export_files_downloader')
    if __logger_initialised:
        return logger

    logger.setLevel(logging.DEBUG)

    # Log DEBUG and INFO to stdout
    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(logging.DEBUG)
    # Only log INFO or lower with this handler
    info_handler.addFilter(lambda record: record.levelno <= logging.INFO)
    logger.addHandler(info_handler)

    # Log WARNING and higher to stderr, include the level and function name
    # in the log message.
    warning_or_error_handler = logging.StreamHandler()
    warning_or_error_handler.setLevel(logging.WARNING)
    warning_or_error_handler.setFormatter(
        logging.Formatter("[{levelname}] {funcName}: {message}", style='{'))
    logger.addHandler(warning_or_error_handler)

    # Mark the logger as initialized, subsequent calls to this function will
    # just return the logger instance.
    __logger_initialised = True

    return logger
