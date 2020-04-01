from glob import glob
from pprint import pprint

from pymongo import MongoClient

from src.merging.steps.loader import Loader

# Settings
MAIN_DB_NAME = 'main'
ext = 'yaml'


yaml_mapping = {
    'FLIGHT': 'flight',
    'DATA': 'dep_data',
    'FF': 'frequent_flyers',
    'FROM': 'dep_short',
    'TO': 'arr_short'
}


class YamlLoader(Loader):
    mapping = yaml_mapping

    def transformation(self, input_dict: dict) -> dict:
        renamed_values = []
        for ff in input_dict['FF']:
            ff['ff'] = ff.pop('CARD')
            renamed_values.append(ff)
        input_dict['FF'] = renamed_values
        return input_dict


if __name__ == "__main__":
    loader = YamlLoader(client=MongoClient('localhost', 27017),
                       db_name='main',
                       collection_name=ext,
                        disable_tqdm=True)
    loader.insert(path=glob(f'../../../../data/{ext}-parsed/*.json'))
    pprint(loader.collection.find_one())
