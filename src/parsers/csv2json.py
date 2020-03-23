import os
import typing

from src.base.parsers import BaseParser

import csv


class CSVParser(BaseParser):
    def parse(self, path: typing.Union[str, os.PathLike], *args, **kwargs):
        with open(path) as f:
            reader = csv.DictReader(f, delimiter=';')
            rows = list(reader)

        output_path = kwargs.get('output_path', self._get_default_output_path(path))
        self.to_json(rows, output_path=output_path)


if __name__ == '__main__':
    a = CSVParser(output_dir="../../data/csv-parsed")
    a.parse('../../../final-project/data/BoardingData.csv')

