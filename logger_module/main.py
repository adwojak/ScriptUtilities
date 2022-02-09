import logging


LOG_FILE_NAME = "logger_file.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"


def setup_logger():
    logging.basicConfig(filename=LOG_FILE_NAME, format=LOG_FORMAT, level=LOG_LEVEL)


if __name__ == "__main__":
    setup_logger()
