import typing

from pymongo import MongoClient
from pymongo.collection import Collection
from tqdm import tqdm


def create_collection(client: MongoClient,
                      db_name: str, name: str) -> Collection:
    """
    Create collection in database db_name.
    Drop whole collection if already exist.
    :param client: mongo client
    :param db_name: database name to place new collection
    :param name: new collection name
    :return: collection
    """
    db = client[db_name]
    if name in db.list_collection_names():
        db[name].drop()
    collection = db[name]
    return collection


def rename_fields(json_objects: typing.Sequence[dict],
                  mapping: dict) -> typing.Sequence[dict]:
    """
    Map object names. If field name is not present in mapping, then it
    goes as is.
    :param json_objects: list of dict objects
    :param mapping: mapping: old_field_name -> new_field_name
    :return: list of renamed fields
    """
    new_objects = []
    for obj in tqdm(json_objects):
        new_objects.append({mapping.get(name, name): val for name, val in obj.items()})

    return new_objects


def set_field(field: str, value: typing.Any) -> dict:
    """
    Return dict used to set field with value in aggregation pipeline
    :param field:
    :param value:
    :return:
    """
    mongo_command = \
        {
            '$set': {
                field: value
            }
        }

    return mongo_command


def create_uid() -> dict:
    """
    Return command used to replace current id by randomly generated
    This command can be used only in aggregation pipeline
    :return: dict with such command
    """
    command = {
                  '$project':
                      {
                          '_id': False
                      }
              }
    return command


def delete_value_from_array(field: str, na_value: str) -> dict:
    return {
        '$set': {
            field: {
                '$filter': {
                    'input': f'${field}',
                    'as': field,
                    'cond': {'$ne': [f'$${field}', na_value]}
                }
            }
        }
    }


def sample(size: int) -> dict:
    return {
        '$sample': {'size': size}
    }