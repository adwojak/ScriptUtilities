import logging


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = "DEBUG"


def setup_logger(logger_file, disable):
    logging.basicConfig(filename=logger_file, format=LOG_FORMAT, level=LOG_LEVEL)
    if disable:
        logging.disable()
