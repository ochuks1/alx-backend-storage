#!/usr/bin/env python3
"""
Module to create an index on the 'name' field in MongoDB collection.
"""

from pymongo import MongoClient

def create_index():
    """Creates an index on the 'name' field in the 'schools' collection."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client.my_db
    school_collection = db.schools
    return school_collection.create_index([("name", 1)])

if __name__ == "__main__":
    print(create_index())
