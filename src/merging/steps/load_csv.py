import json
import os
import typing
from glob import glob

from pymongo import MongoClient

from src.merging.ops import create_collection, rename_fields

path_type = typing.Union[os.PathLike, str]

# Settings
MAIN_DB_NAME = 'main'


csv_mapping = {
    'PassengerSex': 'gender',
    'PassengerBirthDate': 'birth_date',
    'PassengerDocument': 'documents',
    'TicketNumber': 'ticket',
    'FlightDate': 'dep_date',
    'FlightTime': 'dep_time',
    'FlightNumber': 'flight',
    'Destination': 'arr_long'
}


def load_csv_files(client: MongoClient, paths: typing.Sequence[path_type], mapping: dict):
    """
    Insert csv parsed files with mapping to db main in collection csv
    :param client: client to mongo server
    :param paths: path(s) to parsed csv files
    :param mapping: dict-like object that contains name mappings
    :return: db_name, collection_name
    """

    def transformation(input_dict: dict) -> dict:
        first_name = input_dict.get('PassengerFirstName', '')
        second_name = input_dict.get('PassengerSecondName', '')
        last_name = input_dict.get('PassengerLastName', '')
        input_dict['full_name'] = ' '.join((first_name, second_name, last_name))
        return input_dict

    def transform_objects(json_objects: typing.Sequence[dict]) -> typing.Iterable[dict]:
        new_json = rename_fields(json_objects, mapping)
        new_json = map(transformation, new_json)
        return new_json

    def load_one_csv(path: path_type):
        with open(path, 'r') as f:
            json_objs = json.load(f)
        json_objs = transform_objects(json_objs)
        collection.insert_many(json_objs)

    collection = create_collection(client, MAIN_DB_NAME, 'csv')

    if isinstance(paths, str):
        path = paths
        load_one_csv(path)
    elif isinstance(paths, (list, tuple)):
        for path in paths:
            load_one_csv(path)
    else:
        raise TypeError(f"Paths must be list, tuple or str objects, got {type(paths)}")

    return collection


if __name__ == "__main__":
    load_csv_files(client=MongoClient('localhost', 27017),
                   paths=glob('../../data/csv-parsed/*.json'),
                   mapping=csv_mapping)
