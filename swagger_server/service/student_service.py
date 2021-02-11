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
    return student.student_id


def get_student_by_id(student_id, subject):
    student = student_db.get(doc_id=int(student_id))
    
    if subject is None:
        print('1')
        if student:
            print('2')
            return student
        else: 
            print('3')
            return 'Not found', 404

    student = Student.from_dict(student)
    # print('4')
    # if not student.grades
    if subject in student.grades:
        print('5')
        return student
    else:
        print('6')
        return 'Not found', 404


def delete_student(student_id):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student
    student_db.remove(doc_ids=[int(student_id)])
    return student_id

def student_get_by_last_name(last_name):
    print('hoi2')
    if not last_name:
        print('eey')
        return 'Empty lastname', 404
        
    res = student_db.get(Query().last_name == last_name)
    if res:
        print('found')
        return res
    print('ok')