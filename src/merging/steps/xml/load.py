import itertools
from glob import glob
from pprint import pprint

from pymongo import MongoClient

from src.merging.ops import create_uid, rename_fields, set_field, unwind_array_field
from src.merging.steps.loader import Loader

# Settings
MAIN_DB_NAME = 'main'
ext = 'xml'


xml_mapping = dict()


class XMLLoader(Loader):
    mapping = xml_mapping

    def transformation(self, input_dict: dict) -> dict:
        def make_flight_from_card(d):
            ff = d['@number']
            flights = []
            for flight in d['activities']['activity']:
                flights.append({
                    'flight': flight['Code'],
                    'dep_date': flight['Date'],
                    'dep_short': flight['Departure'],
                    'arr_short': flight['Arrival'],
                    'ff': ff
                })

            return flights

        output_dict = dict()
        output_dict['full_name'] = input_dict['name']['@last'] + ' ' + input_dict['name']['@first']
        all_flights = [make_flight_from_card(card) for card in input_dict['cards']['card']]
        output_dict['flights'] = list(itertools.chain(*all_flights))

        return output_dict

    def db_transformation(self):
        unwind_array_field(self.collection, 'flights')


if __name__ == "__main__":
    loader = XMLLoader(client=MongoClient('localhost', 27017),
                       db_name='main',
                       collection_name=ext,
                       disable_tqdm=True)
    loader.insert(path=glob(f'../../../../data/{ext}-parsed/*.json'))
    pprint(loader.collection.find_one())
