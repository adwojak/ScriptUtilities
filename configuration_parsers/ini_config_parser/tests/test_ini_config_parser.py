from configuration_parser.ini_config_parser import IniConfigParser, Section, Parameter


class TestIniConfigParser:
    def config(self, mapping):
        return IniConfigParser("configuration_parsers/tests/test_config.ini", mapping)

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
                int_list=Parameter(name="IntList", cast_type=list, list_elements_type=int, delimiter=";"),
                bool_list=Parameter(name="BoolList", cast_type=list, list_elements_type=bool),
                camel_case_value=Parameter(),
                optional_value=Parameter(name="OptionalValue", default="Optional"),
            )
        }
        assert self.config(mapping).parsed_config == {
            "required_section": {
                "string_value": "Some string",
                "int_value": 1337,
                "bool_value": True,
                "example_list": ["123", "332"],
                "example_list2": ["test", "test2"],
                "example_list3": [6, 4],
                "example_list4": ["test1", "test2"],
                "int_list": [4, 7],
                "bool_list": [True, False, False],
                "camel_case_value": "Some value",
                "optional_value": "Optional",
            }
        }

    def test_missing_section(self):
        mapping = {
            "missing_section": Section(
                "MISSING_SECTION",
                missing_value=Parameter(),
            )
        }
        assert self.config(mapping).errors[0] == "Missing section named MISSING_SECTION in configuration file."

    def test_missing_parameter(self):
        mapping = {"required_section": Section("REQUIRED_SECTION", missing_value=Parameter("MISSING_PARAMETER"))}
        assert self.config(mapping).errors[0] == "Missing parameter named MISSING_PARAMETER in configuration file."

    def test_error_with_casting_type(self):
        mapping = {
            "required_section": Section(
                "REQUIRED_SECTION",
                string_value=Parameter(name="StringValue", cast_type=int),
            )
        }
        assert self.config(mapping).errors[0] == "Parameter StringValue is not of type Integer"

    def test_default_values(self):
        mapping = {
            "required_section": Section(
                "REQUIRED_SECTION",
                optional_parameter=Parameter("OPTIONAL_PARAMETER", default="value"),
            ),
        }
        assert self.config(mapping).parsed_config == {
            "required_section": {
                "optional_parameter": "value",
            }
        }

    def test_multiple_errors(self):
        mapping = {
            "missing_section": Section("MISSING_SECTION"),
            "missing_section2": Section("MISSING_SECTION2"),
            "required_section": Section(
                "REQUIRED_SECTION",
                missing_value=Parameter("MISSING_PARAMETER"),
                missing_value2=Parameter("MISSING_PARAMETER2"),
                string_value=Parameter(name="StringValue", cast_type=int),
            ),
        }
        assert self.config(mapping).errors == [
            "Missing section named MISSING_SECTION in configuration file.",
            "Missing section named MISSING_SECTION2 in configuration file.",
            "Missing parameter named MISSING_PARAMETER in configuration file.",
            "Missing parameter named MISSING_PARAMETER2 in configuration file.",
            "Parameter StringValue is not of type Integer",
        ]

    def test_bool_with_bad_value(self):
        mapping = {
            "bool_with_bad_value": Section(
                "REQUIRED_SECTION",
                bad_value=Parameter(name="BoolListWithBadValue", cast_type=list, list_elements_type=bool),
            )
        }
        assert self.config(mapping).errors[0] == "Elements of list parameter BoolListWithBadValue are not of type Bool"
