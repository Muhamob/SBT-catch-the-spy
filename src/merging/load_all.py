import sys
import os
from glob import glob

from pymongo import MongoClient

from src.merging.steps.csv.load import CSVLoader
from src.merging.steps.json.load import JSONLoader
from src.merging.steps.tab.load import TABLoader
from src.merging.steps.xlsx.load import XLSXLoader
from src.merging.steps.xml.load import XMLLoader
from src.merging.steps.yaml.load import YamlLoader

sys.path.append(os.path.join(os.getcwd(), '../../'))


mapping = {
    'csv': CSVLoader,
    'json': JSONLoader,
    'tab': TABLoader,
    'xlsx': XLSXLoader,
    'xml': XMLLoader,
    'yaml': YamlLoader
}


def load_file(ext: str, data_dir: str, client: MongoClient):
    data_dir_parsed = os.path.join(data_dir, f"{ext}-parsed")
    print(os.path.exists(data_dir_parsed))

    loader = mapping[ext](client=client, db_name='main', collection_name=ext)
    loader.insert(path=glob(os.path.join(data_dir_parsed, "*.json")))

    return loader.collection.find_one()


if __name__ == "__main__":
    exts = list(mapping.keys())
    data_dir = "../../data"
    client = MongoClient('localhost', 27017)

    for ext in exts:
        load_file(ext, data_dir, client)
