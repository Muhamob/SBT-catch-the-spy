import json
import os
import typing

from src.base.parsers import BaseParser


class JSONParser(BaseParser):
    """
    JSON parser used to unify input json and make it list of docs, not
    dict of list of docs
    """
    def parse(self, path: typing.Union[str, os.PathLike], *args, **kwargs):
        with open(path) as f:
            data = json.load(f)

        rows = data['Forum Profiles']
        output_path = kwargs.get('output_path', self._get_default_output_path(path))
        self.to_json(rows, output_path=output_path)


if __name__ == '__main__':
    a = JSONParser(output_dir="../../data/json-parsed")
    a.parse('../../../final-project/data/')

