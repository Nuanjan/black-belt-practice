from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


class Class:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def show_classes(cls):
        query = "SELECT * FROM classes"
        results = connectToMySQL('students_classes_schema').query_db(query)
        classes = []
        for classroom in results:
            classes.append(cls(classroom))

        return classes

    @classmethod
    def get_class_by_id(cls, data):
        query = "SELECT * FROM classes WHERE id = %(id)s"
        results = connectToMySQL(
            'students_classes_schema').query_db(query, data)
        classObj = cls(results[0])
        if len(results) < 1:
            return False
        return classObj

    @classmethod
    def class_with_enrolled_students(cls):
        query = "SELECT classes.id, classes.name, COUNT(students.id) FROM classes JOIN enrollment ON classes.id = enrollment.class_id JOIN students ON students.id = enrollment.student_id GROUP BY classes.id"

        results = connectToMySQL('students_classes_schema').query_db(query)
        classes = []
        for row in results:
            class_data = {
                "id": row['id'],
                "name": row['name'],
                "enrolled_students": row['COUNT(students.id)']
            }
            classes.append(class_data)
        return classes
