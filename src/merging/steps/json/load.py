import itertools
from glob import glob
from pprint import pprint

from pymongo import MongoClient

from src.merging.ops import create_uid, rename_fields, set_field
from src.merging.steps.loader import Loader

# Settings
MAIN_DB_NAME = 'main'
ext = 'json'


json_mapping = dict()


class JSONLoader(Loader):
    mapping = json_mapping

    def transformation(self, input_dict: dict) -> dict:
        def prepare_flights(flights_arr):
            out = []
            for flight in flights_arr:
                out.append({
                    'dep_date': flight['Date'],
                    'arr_long': flight['Arrival']['City'],
                    'arr_short': flight['Arrival']['Airport'],
                    'dep_long': flight['Departure']['City'],
                    'dep_short': flight['Departure']['Airport'],
                    'flight': flight['Flight']
                })
            return out

        def prepare_documents(profile):
            return [d['Passports'] for d in profile['Travel Documents'] if d['Passports'] is not None]

        def prepare_ff(profile):
            return [lp['programm']+lp['Number'] for lp in profile['Loyality Programm']]

        def prepare_full_name(profile):
            last_name = profile['Real Name']['Last Name']
            first_name = profile['Real Name']['First Name']

            if last_name is not None:
                last_name += ' '
            else:
                last_name = ''
            if first_name is None:
                first_name = ''

            return last_name + first_name

        output_dict = dict()
        output_dict['documents'] = prepare_documents(input_dict)
        output_dict['gender'] = input_dict['Sex']
        output_dict['flights'] = prepare_flights(input_dict['Registered Flights'])
        output_dict['full_name'] = prepare_full_name(input_dict)
        output_dict['ff'] = prepare_ff(input_dict)

        return output_dict

    # uncomment below operation to unwind flights
    # def db_transformation(self):
    #     unwind_array_field(self.collection, 'flights')


if __name__ == "__main__":
    loader = JSONLoader(client=MongoClient('localhost', 27017),
                        db_name='main',
                        collection_name=ext,
                        disable_tqdm=True)
    loader.insert(path=glob(f'../../../../data/{ext}-parsed/*.json'))
    pprint(loader.collection.find_one())
