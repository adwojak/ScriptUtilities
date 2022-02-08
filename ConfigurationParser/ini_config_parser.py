from configparser import ConfigParser
from json import loads, JSONDecodeError

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
