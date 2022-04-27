from marshmallow import Schema
from marshmallow.fields import Boolean, String, Float, List, Dict, Nested, IP
from marshmallow.exceptions import ValidationError
from json import load as json_load


class Connection(Schema):
    source = IP(required=True)
    destination = IP(required=True)


class Device(Schema):
    enabled = Boolean(required=True)
    description = String()
    ip = IP(required=True)
    mac = String(required=True)


class Configuration(Schema):
    enabled = Boolean(required=True)
    file_version = Float(data_key="file-version", required=True)
    file_author = String(data_key="file-author")
    file_date = String(data_key="file-date", required=True)
    missing_default = String(load_default="VALUE")
    owners_list = List(String(), data_key="owners-list", required=True)
    connections_list = List(Nested(Connection()), data_key="connections-list", required=True)
    devices_object = Dict(data_key="devices-object", keys=String(), values=Nested(Device()))


with open("config.json") as file_stream:
    json_data = json_load(file_stream)

try:
    config = Configuration().load(json_data)
except ValidationError as error:
    for field, messages in error.messages.items():
        print(f"{field}: {' - '.join(messages)}")
