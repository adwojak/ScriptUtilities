from multiprocessing import Pipe

from configuration_parser.ini_config_parser import IniConfigParser, Section, Parameter
from hot_reload.hot_reload import HotReload

config_files_mappings = {
    "config_file.ini": {
        "section": Section(
            "SECTION",
            number_value=Parameter(name="numberValue", cast_type=int),
            string_value=Parameter(name="stringValue"),
        )
    },
    "other_config_file.ini": {
        "other_section": Section(
            "OTHER_SECTION",
            other_number_value=Parameter("otherNumberValue", cast_type=int),
            other_string_value=Parameter("otherStringValue"),
        )
    },
}


def get_configs(config_files):
    return {
        file: IniConfigParser(file, config_files_mappings[file])
        for file in config_files
    }


def print_configs(configs):
    for key, value in configs.items():
        print(f"{key}: {value.parsed_config}")


if __name__ == "__main__":
    config_files = ["config_file.ini", "other_config_file.ini"]
    output_pipe, input_pipe = Pipe()
    hot_reload = HotReload(config_files, input_pipe)
    hot_reload.run()

    print_configs(get_configs(config_files))

    while True:
        changed_configs = output_pipe.recv()
        print("RELOAD")
        print_configs(get_configs(changed_configs))
