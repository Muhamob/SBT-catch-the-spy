import json
import os
from abc import ABC, abstractmethod
import typing


class BaseParser(ABC):
    """
    Interface for all parsers
    """

    # Parser input format
    input_format: str = "json"

    @abstractmethod
    def parse(self,
              path: typing.Union[str, os.PathLike],
              *args, **kwargs):
        """
        Parse file to intermediate representation
        :param path: path to file which would be parsed
        :param args: additional args
        :param kwargs: additional kwargs
        :return: dict of records
        """
        pass

    @staticmethod
    def to_json(obj,
                output_path: typing.Union[str, os.PathLike],
                *args, **kwargs):
        f = open(output_path, 'w')
        json.dump(obj, f)
        f.close()
