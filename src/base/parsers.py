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
              *args, **kwargs) -> typing.Union[dict, list, tuple]:
        """
        Parse file to intermediate representation
        :param path: path to file which would be parsed
        :param args: additional args
        :param kwargs: additional kwargs
        :return: dict of records
        """
        pass

    def parse_to_json(self,
                      path: typing.Union[str, os.PathLike],
                      *args, **kwargs):
        result = self.parse(path, *args, **kwargs)

        with open(path.replace(f".{self.input_format}", f"_{self.input_format}.json"), 'w') as f:
            json.dump(result, f)
