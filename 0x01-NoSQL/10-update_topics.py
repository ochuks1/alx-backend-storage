#!/usr/bin/env python3
"""
Module to delete documents based on a criteria in MongoDB collection.
"""

from pymongo import MongoClient

def delete_by_criteria():
    """Deletes documents where the 'name' field is 'Holberton'."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client.my_db
    school_collection = db.schools
    return school_collection.delete_many({"name": "Holberton"}).deleted_count

if __name__ == "__main__":
    print(delete_by_criteria())
