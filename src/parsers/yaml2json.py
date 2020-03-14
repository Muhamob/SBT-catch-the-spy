import os
import re
import typing

import yaml

from src.base.parsers import BaseParser


class YamlToJson(BaseParser):

    def parse(self, path: typing.Union[str, os.PathLike], *args, **kwargs):
        file = open(path, 'r')
        current_flight = ""
        current_flight += file.readline()
        current_name = current_flight.rstrip(':\'\n').strip('\'')
        for line in file:
            if re.match("^[\t ]+", line):
                current_flight += line
            else:
                yaml_object = yaml.safe_load(current_flight)
                yaml_to_json_obj = yaml_object[current_name]
                yaml_to_json_obj['DATE'] = current_name
                self.to_json(yaml_to_json_obj, f"json_out/{current_name}.json")
                current_flight = line
                current_name = line.rstrip(':\'\n').strip('\'')
        file.close()


if __name__ == '__main__':
    a = YamlToJson()
    a.parse("SkyTeam-Exchange.yaml")  # PATH TO YAML
