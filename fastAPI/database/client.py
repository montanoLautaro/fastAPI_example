from pymongo import MongoClient

# Base de datos local
# db_client = MongoClient().local


# Base de datos remota para python 3.11 or later
db_client = MongoClient(
    "mongodb+srv://test:test@cluster0.qsxsbmr.mongodb.net/?retryWrites=true&w=majority").test
