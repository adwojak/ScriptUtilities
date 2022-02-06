from ConfigurationParser.ini_config_parser import IniConfigParser, Section, Parameter


class TestIniConfigParser:
    def test_success(self):
        mapping = {
            "required_section": Section(
                "REQUIRED_SECTION",
                string_value=Parameter(name="StringValue"),
                int_value=Parameter(name="IntValue", cast_type=int),
                bool_value=Parameter(name="BoolValue", cast_type=bool),
                example_list=Parameter(name="ExampleList", cast_type=list, delimiter=None),
                example_list2=Parameter(name="ExampleList2", cast_type=list),
                example_list3=Parameter(name="ExampleList3", cast_type=list),
                example_list4=Parameter(name="ExampleList4", cast_type=list, delimiter=";"),
                camel_case_value=Parameter(),
                optional_value=Parameter(name="OptionalValue", default="Optional"),
            )
        }
        config = IniConfigParser("ConfigurationParser/tests/test_config.ini", mapping).parsed_config
        assert config == {
            "required_section": {
                "string_value": "Some string",
                "int_value": 1337,
                "bool_value": True,
                "example_list": ["123", "332"],
                "example_list2": ["test", "test2"],
                "example_list3": [6, 4],
                "example_list4": ["test1", "test2"],
                "camel_case_value": "Some value",
                "optional_value": "Optional",
            }
        }

    def test_missing_section(self):
        pass

    def test_missing_parameter(self):
        pass

    def test_error_with_casting_type(self):
        pass

    def test_default_values(self):
        pass

    def test_list_parsing(self):
        pass
