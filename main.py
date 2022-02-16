from logging import getLogger

from requests import get as rget

from arguments_parser.arguments_parser import parse_arguments
from configuration_parser.ini_config_parser import IniConfigParser, Section, Parameter
from logger_module.logger_module import setup_logger

configuration_mapping = {
    "settings": Section(
        "SETTINGS",
        status_port=Parameter("StatusPort", cast_type=int),
        archive=Parameter("Archive", cast_type=bool),
        version=Parameter("Version", required=False),
        camel_case_param=Parameter(),
    ),
    "ftp": Section(
        "FTP",
        ftp_port=Parameter("FTPPort", cast_type=int),
        ftp_dir=Parameter("FTPDir"),
        su_user_name=Parameter("SUUserName"),
        su_password=Parameter("SUPassword"),
    ),
    "ftps": Section(
        "FTPS",
        required=False,
        run_ftps=Parameter("RunFTPS", cast_type=bool),
        ftp_port=Parameter("FTPPort", cast_type=int, required=False, default=990),
        tftp_dir=Parameter("TFTPDir", required=False),
        values_list=Parameter("ValuesList", cast_type=list, list_elements_type=int, delimiter=";"),
    ),
}

if __name__ == "__main__":
    arguments = parse_arguments()
    setup_logger(arguments["log_file"], arguments["disable_log"])
    logger = getLogger()
    configuration = IniConfigParser(arguments["configuration_file"], configuration_mapping)
    if configuration.errors:
        for error in configuration.errors:
            logger.error(error)
        exit(f"Errors while reading configuration file. Check {arguments['log_file']} for more details")
    config = configuration.parsed_config
    response = rget("https://httpbin.org/ip")
    origin_ip = response.json()["origin"]
    logger.info(origin_ip)
    print(origin_ip)
