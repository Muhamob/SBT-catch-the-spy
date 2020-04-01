import json
import os
import typing
from abc import ABC, abstractmethod

from pymongo import MongoClient
from pymongo.collection import Collection
from tqdm import tqdm

from src.base import loggers
from src.merging.ops import create_collection, rename_fields

PathType = typing.Union[os.PathLike, str]


class Loader(ABC):
    # field mapping dictionary: ol_field_name -> new_field_name
    mapping: dict = dict()
    logger = loggers.get_logger()

    def __init__(self,
                 client: MongoClient,
                 db_name: str,
                 collection_name: str,
                 disable_tqdm: bool = False):
        self.client: MongoClient = client
        self.db_name: str = db_name
        self.collection_name: str = collection_name

        # create collection, drop if not empty
        self.collection: Collection = create_collection(client, db_name, collection_name)

        # tqdm settings
        self.disable_tqdm: bool = disable_tqdm

    def insert(self, path: typing.Union[PathType, typing.Iterable[PathType]]):
        """
        Insert all files from path. If path is a str then put only one file.
        If iterable, the put all
        :param path: path-like or iterable of path like
        :return: None
        """
        if isinstance(path, str):
            self.logger.debug(f"Got only one file")
            self.insert_one_file(path)
        elif isinstance(path, (list, tuple)):
            paths = path
            self.logger.debug(f"Got {len(paths)} files")
            for path in paths:
                self.insert_one_file(path)
        else:
            self.logger.error(f"Paths must be list, tuple or str objects, got {type(path)}")
            raise TypeError(f"Paths must be list, tuple or str objects, got {type(path)}")

    def insert_one_file(self, path: PathType):
        json_objs = self.load_one_file(path)
        json_objs = self.transform(json_objs)
        json_objs = rename_fields(json_objs, self.mapping)
        self.collection.insert_many(json_objs)

    def load_one_file(self, path: PathType) -> typing.List[dict]:
        self.logger.info(f"Loading file {path}")

        try:
            with open(path, 'r') as f:
                json_objs = json.load(f)
            self.logger.info(f"File loaded. Total count: {len(json_objs)} documents")
        except FileExistsError as e:
            self.logger.error(e)
            json_objs = []

        return json_objs

    def transform(self, json_objects: typing.Iterable[dict]) -> typing.Iterable[dict]:
        self.logger.info("Applying transformation")
        return map(self.transformation, self.pbar(json_objects))

    @abstractmethod
    def transformation(self, input_dict: dict) -> dict:
        pass

    def pbar(self, iterable: typing.Iterable, **kwargs):
        """
        Get progress bar
        :param iterable:
        :param kwargs: dict of arguments to put in tqdm
        :return:
        """
        return tqdm(iterable, disable=self.disable_tqdm, **kwargs)


