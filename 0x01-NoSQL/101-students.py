#!/usr/bin/env python3
"""
Module to return all students sorted by average score.
"""

from pymongo import MongoClient

def top_students(mongo_collection):
    """Returns all students sorted by average score."""
    students = list(mongo_collection.find())
    
    for student in students:
        topics = student.get('topics', [])
        total_score = sum(topic.get('score', 0) for topic in topics)
        average_score = total_score / len(topics) if topics else 0
        student['averageScore'] = average_score
    
    return sorted(students, key=lambda x: x['averageScore'], reverse=True)
