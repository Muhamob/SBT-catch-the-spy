from pymongo import MongoClient

import typing


class Loader:
    def __init__(self, client: MongoClient, db_name: str, collection_name: str):
        self.__client: MongoClient = client
        self.__db = client[db_name]
        self.__collection = self.__db[collection_name]

    def load(self, obj: typing.Union[dict, typing.Sequence[dict]]):
        if isinstance(obj, dict):
            self.__collection.insert_one(obj)
        elif isinstance(obj, (list, tuple)):
            self.__collection.insert_many(obj)
        else:
            raise ValueError(f"Obj must be either dict or sequence, got {type(obj)}")


if __name__ == "__main__":
    import glob
    import json
    from tqdm import tqdm

    client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=1000)
    xlsx_saver = Loader(client, 'main', 'xlsx')

    for path in tqdm(glob.glob("../../data/xlsx-parsed/*.json")):
        with open(path, 'r') as f:
            obj = json.load(f)

        assert isinstance(obj, (dict, list, tuple)), f"Obj must be dict, tuple or list. Got {type(obj)}"
        xlsx_saver.load(obj)
