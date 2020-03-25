import json
import os
import typing
from abc import ABC, abstractmethod

from src.base import loggers


class BaseParser(ABC):
    """
    Interface for all parsers
    """

    # Parser input format
    input_format: str = "json"
    logger = loggers.logger

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

    def to_json(self,
                obj,
                output_path: typing.Union[str, os.PathLike],
                *args, **kwargs):
        self.logger.info(f"Running {self.__class__.__name__} parser, saving json")
        f = open(output_path, 'w')
        json.dump(obj, f, *args, **kwargs, indent=4)
        f.close()
        self.logger.info("Saved")
