#!/usr/bin/env python3
"""
Module to update documents with multiple criteria in MongoDB collection.
"""

from pymongo import MongoClient

def update_with_criteria():
    """Updates documents where 'name' starts with 'H' and 'city' field exists."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client.my_db
    school_collection = db.schools
    return school_collection.update_many(
        {"name": {"$regex": "^H"}, "city": {"$exists": True}},
        {"$set": {"updated": True}}
    ).modified_count

if __name__ == "__main__":
    print(update_with_criteria())
