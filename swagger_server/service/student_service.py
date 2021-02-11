import json
import logging
import os
import tempfile

from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from functools import reduce
import uuid

from swagger_server.models import Student

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


def add_student(student):
    if not student.first_name:
        return 'Firstname is empty', 405
    if not student.last_name:
        return 'Lastname is empty', 405
        
    print("test")
    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    print(student.student_id)
    print(student.to_dict())
    return student.student_id


def get_student_by_id(student_id, subject):
    print('hoi')
    print(student_id)
    student = student_db.get(doc_id=int(student_id))
    
    if subject is None:
        print(student)
        print(not student)
        if student:
            return student
        else: 
            return 'Not found', 404

    student = Student.from_dict(student)
    if subject in student.grades:
        return student
    else:
        return 'Not found', 404


def delete_student(student_id):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student
    student_db.remove(doc_ids=[int(student_id)])
    return student_id
