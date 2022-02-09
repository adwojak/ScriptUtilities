from argparse import ArgumentParser


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("configuration_file", type=str, help="Configuration file used for script")
    parser.add_argument("--disable_log", action="store_true", help="Disable log gathering")
    parser.add_argument(
        "--log_file",
        type=str,
        default="logger_file.log",
        help="Location for log file. Must be .txt or .log. If not provided, log file will be created in same directory as script",
    )
    return vars(parser.parse_args())
