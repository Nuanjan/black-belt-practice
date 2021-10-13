# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{8,}\Z')


class Student:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.classes = []

    @staticmethod
    def validate_student(studentFormData):
        is_valid = True  # we assume this is true
        if len(studentFormData['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if len(studentFormData['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False

        if len(studentFormData['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if not PW_REGEX.match(studentFormData['password']):
            flash("email must contain at least one digit")
            flash("email must contain at least one uppercase letter")
            flash("email must contain at least one lowercase letter")
            is_valid = False
        if studentFormData['password'] != studentFormData['confirm_password']:
            flash("Password and confirm password does not match")
            is_valid = False
        if not EMAIL_REGEX.match(studentFormData['e_mail']):
            flash("Invalid email")
            is_valid = False
        data = {"email": studentFormData['e_mail']}
        if Student.get_student_by_email(data):
            flash("This Email already taken!")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login_student(data):
        is_valid = True
        if not data['student_in_db']:
            flash("Incorrect Email/Password")
            is_valid = False
        return is_valid

    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM students;"
    #     # make sure to call the connectToMySQL function with the schema you are targeting.
    #     results = connectToMySQL('students_schema').query_db(query)
    #     # Create an empty list to append our instances of students
    #     students = []
    #     # Iterate over the db results and create instances of students with cls.
    #     for student in results:
    #         students.append(cls(student))
    #     return students

    @classmethod
    def add_student(cls, data):
        print('data from queries: ', data)
        query = "INSERT INTO students (first_name , last_name , email ,password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s, NOW() , NOW());"
        return connectToMySQL('students_classes_schema').query_db(query, data)

    # @classmethod
    # def get_student_with_recipes(cls, data):
    #     query = "SELECT * FROM students LEFT JOIN recipes ON students.id = recipes.student_id WHERE students.id = %(id)s"
    #     results = connectToMySQL('students_classes_schema').query_db(query, data)
    #     print(results[0])
    #     student = cls(results[0])

    #     for row in results:
    #         recipe_data = {
    #             "id": row['recipes.id'],
    #             "name": row['name'],
    #             "description": row['description'],
    #             "instructions": row['instructions'],
    #             "date_made": row['date_made'],
    #             "time_cook": row['time_cook'],
    #             "created_at": row['recipes.created_at'],
    #             "updated_at": row['recipes.updated_at'],
    #             "student_id": row['student_id']
    #         }
    #         student.recipes.append(recipe.Recipe(recipe_data))

    #     return student

    # @classmethod
    # def edit_student(cls, data):
    #     print(data, " this is data before query")
    #     query = "UPDATE students SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE students.id = %(id)s"
    #     # data is a dictionary that will be passed into the save method from server.py
    #     # will return the id of that data that we just insert in

    #     return connectToMySQL('students_schema').query_db(query, data)

    # @classmethod
    # def delete_student(cls, data):
    #     query = "DELETE FROM students WHERE students.id = %(id)s;"
    #     return connectToMySQL('students_schema').query_db(query, data)

    @classmethod
    def get_student_by_email(cls, data):
        query = "SELECT * FROM students WHERE email = %(email)s"
        result = connectToMySQL('students_classes_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_student_by_id(cls, data):
        query = "SELECT * FROM students WHERE students.id = %(id)s"
        result = connectToMySQL('students_classes_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
