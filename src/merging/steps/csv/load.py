import json
import os
import typing
from glob import glob
from pprint import pprint

from pymongo import MongoClient

from src.merging.ops import create_collection, rename_fields
from src.merging.steps.loader import Loader

PathType = typing.Union[os.PathLike, str]

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


class CSVLoader(Loader):
    mapping = csv_mapping

    def transformation(self, input_dict: dict) -> dict:
        first_name = input_dict.get('PassengerFirstName', '')
        second_name = input_dict.get('PassengerSecondName', '')
        last_name = input_dict.get('PassengerLastName', '')
        input_dict['full_name'] = ' '.join((first_name, second_name, last_name))
        return input_dict


if __name__ == "__main__":
    loader = CSVLoader(client=MongoClient('localhost', 27017),
                       db_name='main',
                       collection_name='csv')
    loader.insert(path=glob('../../../../data/csv-parsed/*.json'))
    pprint(loader.collection.find_one())