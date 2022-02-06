from configparser import ConfigParser
from json import loads, JSONDecodeError


class Parameter:
    def __init__(self, name=None, required=True, default=None, cast_type=str, delimiter=","):
        self.name = name
        self.required = required
        self.default = default
        self.cast_type = cast_type
        self.delimiter = delimiter

    def parse_parameter(self, parameter_value):
        # TODO Error with casting types
        if self.cast_type == list:
            return self.cast_to_list(parameter_value)
        return self.cast_type(parameter_value)

    def cast_to_list(self, parameter_value):
        try:
            return loads(parameter_value)
        except JSONDecodeError:
            return parameter_value.split(self.delimiter)


class Section:
    def __init__(self, name=None, required=True, **parameters):
        self.name = name
        self.required = required
        self.parameters = parameters

    def parse_section(self, section):
        section_parsed = {}
        for key, parameter in self.parameters.items():
            # TODO Error if missing parameter
            parameter_name = parameter.name or key
            parameter_value = section.get(parameter_name, parameter.default)
            if parameter_value:
                section_parsed[key] = parameter.parse_parameter(parameter_value)
        return section_parsed


class IniConfigParser(ConfigParser):
    def __init__(self, path, config_mapping, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read(path)
        self.parsed_config = self.parse_config(config_mapping)

    def parse_config(self, config_mapping):
        configuration = {}
        for key, section in config_mapping.items():
            # TODO Error if missing section
            section_name = section.name or key
            configuration[key] = section.parse_section(self[section_name])
        return configuration
