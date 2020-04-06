import collections
import os

import xmltodict
import typing

from src.base.parsers import BaseParser


class XMLParser(BaseParser):
    def parse(self, path: typing.Union[str, os.PathLike], *args, **kwargs):
        with open(path, 'r') as f:
            doc = xmltodict.parse(f.read(), process_namespaces=True)
            rows = doc['PointzAggregatorUsers']['user']

        for user in rows:
            card = user['cards']['card']
            if isinstance(card, collections.OrderedDict):
                card_list = list()
                card_list.append(card)
                user['cards']['card'] = card_list
                print(type(user['cards']['card']))

        output_path = kwargs.get('output_path', self._get_default_output_path(path))
        #output_path = "output.json"
        self.to_json(rows, output_path=output_path)


if __name__ == '__main__':
    xml_parser = XMLParser(output_dir="../../data/xml-parsed/")
    xml_parser.parse("PointzAggregator-AirlinesData.xml")  # PATH TO  XML
