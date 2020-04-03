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

    def __init__(self, output_dir: typing.Union[str, os.PathLike]):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            self.logger.info(f"{output_dir} doesn't exist, running !mkdir -p {output_dir}")
            os.makedirs(output_dir)

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
        self.logger.info(f"Successful; path: {output_path}")

    def _get_default_output_path(self, path: typing.Union[str, os.PathLike]):
        base, filename = os.path.split(path)
        name, ext = os.path.splitext(filename)
        return os.path.join(self.output_dir, f'{name}.json')
