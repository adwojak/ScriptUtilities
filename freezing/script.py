import logging
from argparse import ArgumentParser
from configparser import ConfigParser
from json import loads, JSONDecodeError
from logging import getLogger

from requests import get as rget

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = "DEBUG"


def setup_logger(logger_file, disable):
    logging.basicConfig(filename=logger_file, format=LOG_FORMAT, level=LOG_LEVEL)
    if disable:
        logging.disable()


TYPE_TO_STRING_MAP = {int: "Integer", str: "String", bool: "Boolean", float: "Float", bytes: "Bytes", list: "List"}


class NonBoolError(Exception):
    pass


class Parameter:
    def __init__(self, name=None, required=True, default=None, cast_type=str, list_elements_type=str, delimiter=","):
        self.name = name
        self.required = required
        self.default = default
        self.cast_type = cast_type
        self.list_elements_type = list_elements_type
        self.delimiter = delimiter

    def parse_parameter(self, parameter_value):
        if self.cast_type == list:
            return self.cast_to_list(parameter_value)
        elif self.cast_type == bool:
            return self.string_to_bool(parameter_value)
        return self.cast_type(parameter_value)

    def cast_to_list(self, parameter_value):
        try:
            return loads(parameter_value)
        except JSONDecodeError:
            if self.list_elements_type == bool:
                return [self.string_to_bool(element) for element in parameter_value.split(self.delimiter)]
            return [self.list_elements_type(element) for element in parameter_value.split(self.delimiter)]

    def string_to_bool(self, value):
        value = value.lower()
        if value in ("y", "yes", "t", "true", "on", "1"):
            return True
        elif value in ("n", "no", "f", "false", "off", "0"):
            return False
        else:
            if self.cast_type == list:
                raise NonBoolError
            raise ValueError


class Section:
    def __init__(self, name=None, required=True, **parameters):
        self.errors = []
        self.name = name
        self.required = required
        self.parameters = parameters

    def parse_section(self, section):
        section_parsed = {}
        for key, parameter in self.parameters.items():
            parameter_name = parameter.name or key
            parameter_value = section.get(parameter_name, parameter.default)
            if parameter_value is None:
                self.errors.append(f"Missing parameter named {parameter_name} in configuration file.")
            else:
                try:
                    section_parsed[key] = parameter.parse_parameter(parameter_value)
                except ValueError:
                    self.errors.append(
                        f"Parameter {parameter_name} is not of type {TYPE_TO_STRING_MAP[parameter.cast_type]}"
                    )
                except NonBoolError:
                    self.errors.append(f"Elements of list parameter {parameter_name} are not of type Bool")
        return section_parsed


class IniConfigParser(ConfigParser):
    def __init__(self, path, config_mapping, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.read(path)
        self.parsed_config = self.parse_config(config_mapping)

    def parse_config(self, config_mapping):
        configuration = {}
        for key, section in config_mapping.items():
            section_name = section.name or key
            if section_name not in self.sections():
                if section.required:
                    self.errors.append(f"Missing section named {section_name} in configuration file.")
            else:
                configuration[key] = section.parse_section(self[section_name])
            self.errors.extend(section.errors)
        return configuration


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
