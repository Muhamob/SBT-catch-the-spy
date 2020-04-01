from glob import glob
from pprint import pprint

from pymongo import MongoClient

from src.merging.steps.loader import Loader

# Settings
MAIN_DB_NAME = 'main'
ext = 'xlsx'


xlsx_mapping = {
    'name_surname': 'full_name',
    'TravelDoc': 'documents',
    'departure': 'dep_long',
    'arrival': 'arr_long',
    'ticket_num': 'ticket'
    # TODO: добавить поле gender на основе поля name_prefix
}


class XLSXLoader(Loader):
    mapping = xlsx_mapping

    def transformation(self, input_dict: dict) -> dict:
        return input_dict


if __name__ == "__main__":
    loader = XLSXLoader(client=MongoClient('localhost', 27017),
                        db_name='main',
                        collection_name=ext,
                        disable_tqdm=True)
    loader.insert(path=glob(f'../../../../data/{ext}-parsed/*.json'))
    pprint(loader.collection.find_one())
