import json
import os
import typing
from glob import glob
from pprint import pprint

from pymongo import MongoClient

from src.merging.ops import create_collection, rename_fields

path_type = typing.Union[os.PathLike, str]

# Settings
MAIN_DB_NAME = 'main'


tab_mapping = {
    'PaxName': 'full_name',
    'PaxBirthDate': 'birth_date',
    'TravelDoc': 'documents',
    'e_Ticket': 'ticket',
    'DepartDate': 'dep_date',
    'DepartTime': 'dep_time',
    'ArrivalDate': 'dep_date',
    'ArrivalTime': 'dep_time',
    'From': 'dep_short',
    'Dest': 'arr_short',
    'FF': 'ff'
}


def load_tab_files(client: MongoClient, paths: typing.Sequence[path_type], mapping: dict):
    """
    Insert tab parsed files with mapping to db main in collection tab
    :param client: client to mongo server
    :param paths: path(s) to parsed tab files
    :param mapping: dict-like object that contains name mappings
    :return: db_name, collection_name
    """

    def transformation(input_dict: dict) -> dict:
        return input_dict

    def transform_objects(json_objects: typing.Sequence[dict]) -> typing.Iterable[dict]:
        new_json = rename_fields(json_objects, mapping)
        new_json = map(transformation, new_json)
        return new_json

    def load_one_tab(path: path_type):
        with open(path, 'r') as f:
            json_objs = json.load(f)
        json_objs = transform_objects(json_objs)
        collection.insert_many(json_objs)

    collection = create_collection(client, MAIN_DB_NAME, 'tab')

    if isinstance(paths, str):
        path = paths
        load_one_tab(path)
    elif isinstance(paths, (list, tuple)):
        for path in paths:
            load_one_tab(path)
    else:
        raise TypeError(f"Paths must be list, tuple or str objects, got {type(paths)}")

    return collection


if __name__ == "__main__":
    tab = load_tab_files(client=MongoClient('localhost', 27017),
                   paths=glob('../../../../data/tab-parsed/*.json'),
                   mapping=tab_mapping)
    pprint(tab.find_one())