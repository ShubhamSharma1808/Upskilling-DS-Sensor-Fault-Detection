from sensor.configs.mongo_db_Connection import MongoDBClient


if __name__ == '__main__':
    mongoDb_client = MongoDBClient()
    print(mongoDb_client.database.list_collection_names())
    