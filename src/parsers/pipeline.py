import os
import typing

from src.base.loggers import logger
from src.base.parsers import BaseParser
from src.parsers import *

path_type = typing.Union[str, os.PathLike]


class Pipeline:
    logger = logger

    def __init__(self, parsers: typing.Mapping[str, BaseParser]):
        self.parsers = parsers

    def get_parser(self, filename: path_type):
        name, ext = os.path.splitext(filename)
        ext = ext[1:]  # delete dot in front of extension name
        parser = self.parsers.get(ext, None)

        if parser is None:
            self.logger.warning(f"Cannot find suitable parser for file {filename}")
            return None
        else:
            self.logger.info(f"Using parser {parser.__class__.__name__}")
            return parser

    def parse_dir(self, dir_path: path_type):
        for filename in os.listdir(dir_path):
            if not os.path.isdir(filename):
                self.parse_file(os.path.join(dir_path, filename))

    def parse_file(self, path: path_type):
        base, filename = os.path.split(path)
        self.logger.info(f"Attempt to parse file {filename}")
        parser = self.get_parser(filename)

        if parser is None:
            self.logger.error("Cannot parse file [x]")
        else:
            try:
                self.logger.info(f"Start parsing {filename} ...")
                parser.parse(path)
                self.logger.info(f"Successfully parsed files [Ok]")
            except Exception as e:
                self.logger.error(f"Cannot parse file")


def get_default_pipeline():
    parsers = {
        'xml': XMLParser(output_dir="../../data/xml-parsed"),
        'xlsx': XLSXParser(output_dir="../../data/xlsx-parsed"),
        'tab': TABParser(output_dir="../../data/tab-parsed"),
        'csv': CSVParser(output_dir="../../data/csv-parsed"),
        'yaml': YAMLParser(output_dir="../../data/yaml-parsed"),
        'json': JSONParser(output_dir="../../data/json-parsed")
    }

    return Pipeline(parsers)


if __name__ == "__main__":
    pipeline = get_default_pipeline()
    pipeline.parse_dir("../../../final-project/data")
