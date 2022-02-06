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
    ),
    "ftp": Section(
        "FTPXXX",
        missing_param=Parameter("something")
    ),
    "ftp2": Section(
        "FTPXXX2222",
        required=False,
        missing_param=Parameter("something")
    )
}


if __name__ == "__main__":
    # For testing purposes
    config = IniConfigParser("ConfigurationParser/configuration.ini", config_mapping)
    print(config.parsed_config)
    print(config.errors)
