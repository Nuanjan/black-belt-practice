from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


class Enrollment:
    def __init__(self, data):
        self.id = data['id']
        self.student_id = data['student_id']
        self.class_id = data['class_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_student_to_class(cls, data):
        query = "INSERT INTO enrollment(student_id, class_id, created_at, updated_at) VALUES(%(student_id)s, %(class_id)s, NOW(),NOW())"
        return connectToMySQL('students_classes_schema').query_db(query, data)
