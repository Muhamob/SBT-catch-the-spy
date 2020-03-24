import os
import re
import typing

import yaml
import json

from src.base.parsers import BaseParser


class YamlToJson(BaseParser):

    def parse(self, path: typing.Union[str, os.PathLike], *args, **kwargs):
        file = open(path, 'r')
        directory = "yaml/json_out/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        current_flight = ""
        current_flight += file.readline()
        current_name = current_flight.rstrip(':\'\n').strip('\'')
        for line in file:
            if re.match("^[\t ]+", line):
                current_flight += line
            else:
                yaml_object = yaml.safe_load(current_flight)
                yaml_to_json_obj = yaml_object[current_name]
                self.to_json(yaml_to_json_obj, f"{directory}{current_name}.json")
                current_flight = line
                current_name = line.rstrip(':\'\n').strip('\'')
        file.close()

    @staticmethod
    def convert_to_arrays_of_json(json_dict, data):
        result_json_array = []
        current_dict = {}
        for keys, vals in json_dict.items():
            current_dict['FLIGHT'] = keys
            current_dict['DATA'] = data
            current_array = []
            for keys_, vals_ in vals.items():
                if keys_ == 'FF':
                    for keys__, vals__ in vals_.items():
                        current_val_dict = {'CARD': keys__}
                        for keys___, vals___ in vals__.items():
                            current_val_dict[keys___] = vals___
                        current_array.append(current_val_dict)
                    pass
                else:
                    current_dict[keys_] = vals_
                current_dict['FF'] = current_array
            result_json_array.append(current_dict)
            current_dict = {}
        return result_json_array


if __name__ == '__main__':
    a = YamlToJson()
    a.parse("yaml/SkyTeam-Exchange.yaml")  # PATH TO YAML
    entries = os.listdir('yaml/json_out/')
    array_directory = "yaml/json_array_out/"
    if not os.path.exists(array_directory):
        os.makedirs(array_directory)
    for entry in entries:
        with open('yaml/json_out/' + entry, 'r') as json_file:
            json_array_data = a.convert_to_arrays_of_json(json.load(json_file), entry.split('.')[0])
            with open(f"{array_directory}{entry}", "w") as write_file:
                json.dump(json_array_data, write_file)
