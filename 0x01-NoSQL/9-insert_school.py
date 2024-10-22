#!/usr/bin/env python3
"""
Module to find all documents with a projection in MongoDB collection.
"""

from pymongo import MongoClient

def find_with_projection():
    """Finds all documents but only returns the 'name' field."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client.my_db
    school_collection = db.schools
    return list(school_collection.find({}, {"name": 1, "_id": 0}))

if __name__ == "__main__":
    for school in find_with_projection():
        print(school)
