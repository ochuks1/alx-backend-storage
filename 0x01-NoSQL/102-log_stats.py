#!/usr/bin/env python3
"""
Module to print log statistics from the nginx collection.
"""

from pymongo import MongoClient
from collections import Counter

def log_stats():
    """Prints log statistics."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs

    total_logs = db.nginx.count_documents({})
    print(f"{total_logs} logs")

    methods = db.nginx.aggregate([
        { "$group": { "_id": "$method", "count": { "$sum": 1 } } }
    ])
    print("Methods:")
    for method in methods:
        print(f"    method {method['_id']}: {method['count']}")

    status_check = db.nginx.aggregate([
        { "$group": { "_id": "$status", "count": { "$sum": 1 } } }
    ])
    total_status = sum(item['count'] for item in status_check)
    print(f"{total_status} status check")

    ip_addresses = db.nginx.aggregate([
        { "$group": { "_id": "$ip", "count": { "$sum": 1 } } },
        { "$sort": { "count": -1 } },
        { "$limit": 10 }
    ])

    print("IPs:")
    for ip in ip_addresses:
        print(f"    {ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    log_stats()
