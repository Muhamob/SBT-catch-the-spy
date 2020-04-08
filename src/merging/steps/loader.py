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
    """
    Class used to load dataset to Mongo DB.
    To create loader for your file you only need to specify two things:
        1. mapping - that is mapping between old field names and common field names
        2. transformation - function that makes transformation on single document of your collection
    After that you only need to init class with Mongo client, db name and collection name and call
    insert.
    """
    # field mapping dictionary: ol_field_name -> new_field_name
    mapping: dict = dict()

    # default logger
    logger = loggers.get_logger()

    def __init__(self,
                 client: MongoClient,
                 db_name: str,
                 collection_name: str,
                 disable_tqdm: bool = False):
        self.client: MongoClient = client
        # by default use db_name = main
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

        # Make final transformation in database
        self.db_transformation()

        total_count = self.collection.count_documents({})
        self.logger.info(f"Total count of documents in collection {self.collection_name} is {total_count}")

    def insert_one_file(self, path: PathType):
        """
        Defines the pipeline of inserting one file (list of documents)
        Default pipeline is:
            1. load file from disk
            2. apply transformation on each document in this file
            3. apply field mapping on each document
            4. finally, insert these documents to collection
        :param path: path to json file, that contains list of documents
        :return: None
        """
        json_objs = self.load_one_file(path)
        json_objs = self.transform(json_objs)
        json_objs = rename_fields(json_objs, self.mapping)
        self.collection.insert_many(json_objs)

    def load_one_file(self, path: PathType) -> typing.List[dict]:
        """
        Load one file from disk
        :param path: path to json file with list of documents
        :return: list of documents
        """
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
        """
        Method that applies transformation to each document
        :param json_objects: list of documents(dicts)
        :return: iterable of transformed documents
        """
        self.logger.info("Applying transformation")
        return map(self.transformation, self.pbar(json_objects))

    @abstractmethod
    def transformation(self, input_dict: dict) -> dict:
        """
        This is the only method you need to define. THis method takes a
        document and transform it
        :param input_dict:
        :return:
        """
        pass

    def pbar(self, iterable: typing.Iterable, **kwargs):
        """
        Get progress bar
        :param iterable:
        :param kwargs: dict of arguments to put in tqdm
        :return:
        """
        # tqdm_out = TqdmToLogger(self.logger, level=logging.INFO)
        return tqdm(iterable, disable=self.disable_tqdm, **kwargs)

    def db_transformation(self):
        """
        Make a request in database and perform transformation in it
        :return: None
        """
        pass
