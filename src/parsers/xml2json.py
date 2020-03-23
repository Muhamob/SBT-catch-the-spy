import os

import xmltodict
import typing

from src.base.parsers import BaseParser


class XMLToJson(BaseParser):
    def parse(self, path: typing.Union[str, os.PathLike], *args, **kwargs):
        with open(path, 'r') as f:
            doc = xmltodict.parse(f.read(), process_namespaces=True)
            rows = doc['PointzAggregatorUsers']['user']
        output_path = kwargs.get('output_path', '../../data/xml-parsed/PointzAggregator-AirlinesData.json')
        self.to_json(rows, output_path=output_path)


if __name__ == '__main__':
    xml_parser = XMLToJson()
    xml_parser.parse("PointzAggregator-AirlinesData.xml")  # PATH TO YAML