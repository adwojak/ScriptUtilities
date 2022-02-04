from ConfigurationParser.ini_config_parser import IniConfigParser, Section, Parameter


config_mapping = {
    "settings": Section(
        "SETTINGS",
        status_port=Parameter("StatusPort", cast_type=int),
        archive=Parameter("Archive", cast_type=int),
        log_file=Parameter("LogFile"),
        version=Parameter("Version"),
        optional=Parameter("Optional", required=False, default="Optional value"),
        second_optional=Parameter(required=False),
        camel_case_param=Parameter(),
    )
}


if __name__ == "__main__":
    # For testing purposes
    config = IniConfigParser("ConfigurationParser/configuration.ini", config_mapping).parsed_config
    print(config)
