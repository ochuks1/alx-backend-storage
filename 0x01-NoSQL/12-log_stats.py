#!/usr/bin/env python3
"""
Module to aggregate documents in MongoDB collection.
"""

from pymongo import MongoClient

def aggregate():
    """Performs aggregation on documents in the 'schools' collection."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client.my_db
    school_collection = db.schools
    pipeline = [
        {"$match": {"city": "San Francisco"}},
        {"$group": {"_id": "$city", "total": {"$sum": 1}}}
    ]
    return list(school_collection.aggregate(pipeline))

if __name__ == "__main__":
    for result in aggregate():
        print(result)
