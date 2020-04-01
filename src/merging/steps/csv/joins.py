from pprint import pprint

from pymongo import MongoClient, CursorType

from src.merging.ops import set_field, create_uid, delete_value_from_array, sample


def group_by_document(client: MongoClient, db_name: str,
                      csv_collection_name: str, output_collection_name: str) -> CursorType:
    db = client[db_name]
    csv_collection = db[csv_collection_name]
    assert csv_collection.count_documents({}) > 0,  "Check out your csv collection, as it is empty"

    result = csv_collection.aggregate([
        # # sampling is used to speed up prototyping
        # sample(1000),
        {
            # group by document
            '$group': {
                '_id': '$documents',
                'full_name': {'$addToSet': '$full_name'},
                'gender': {'$addToSet': '$gender'},
                'birth_date': {'$addToSet': '$birth_date'},
                # create new field flights, that contains list of flights
                'flights': {
                    '$push': {
                        'BookingCode': '$BookingCode',
                        'ticket': '$ticket',
                        'Baggage': '$Baggage',
                        'dep_date': '$dep_date',
                        'dep_time': '$dep_time',
                        'flight': '$flight',
                        'CodeShare': '$CodeShare',
                        'arr_long': '$arr_long'
                    }
                },
                'tickets': {'$addToSet': '$ticket'},
            }
        },
        # create new field ff
        set_field('ff', []),
        # explicitly add new field which is copied from _id
        set_field('documents', '$_id'),
        # delete "Not presented" in tickets field
        delete_value_from_array('tickets', 'Not presented'),
        # Make unique identifier based on random, not on document
        create_uid(),
        {'$out': output_collection_name}
    ], allowDiskUse=True)

    return result


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    group_by_document(client, 'main', 'csv', 'csv_joined')
    csv_joined = client['main']['csv_joined']
    pprint(csv_joined.find_one())
