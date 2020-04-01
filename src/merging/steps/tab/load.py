from glob import glob
from pprint import pprint

from pymongo import MongoClient

from src.merging.steps.loader import Loader

# Settings
MAIN_DB_NAME = 'main'


tab_mapping = {
    'PaxName': 'full_name',
    'PaxBirthDate': 'birth_date',
    'TravelDoc': 'documents',
    'e_Ticket': 'ticket',
    'DepartDate': 'dep_date',
    'DepartTime': 'dep_time',
    'ArrivalDate': 'arr_date',
    'ArrivalTime': 'arr_time',
    'From': 'dep_short',
    'Dest': 'arr_short',
    'FF': 'ff'
}


class TABLoader(Loader):
    mapping = tab_mapping

    def transformation(self, input_dict: dict) -> dict:
        return input_dict


if __name__ == "__main__":
    loader = TABLoader(client=MongoClient('localhost', 27017),
                       db_name='main',
                       collection_name='tab')
    loader.insert(path=glob('../../../../data/tab-parsed/*.json'))
    pprint(loader.collection.find_one())
