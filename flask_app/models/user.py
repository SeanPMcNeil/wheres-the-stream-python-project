from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Optional Regex to Check for more complex passwords
# PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.movies = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username, email, password, created_at, updated_at) VALUES (%(username)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL("stream_schema").query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s"
        result = connectToMySQL('stream_schema').query_db(query, data)
        return User(result[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('stream_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET username = %(username)s, email = %(email)s, updated_at = NOW() WHERE id = %(user_id)s;"
        connectToMySQL('stream_schema').query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True

        # First Name Check
        if not user['username'].isalpha() or len(user['username']) < 3:
            flash(u"Username must be only letters AND at least 3 characters", "registration")
            is_valid = False
        
        # Email Check
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('stream_schema').query_db(query, user)
        print(results)
        if len(results) >= 1:
            flash(u'Email is already registered', "registration")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash(u"Invalid email address!", "registration")
            is_valid = False

        # Password Length Check
        if len(user['password']) < 8:
            flash(u"Password must be at least 8 characters", "registration")
            is_valid = False

        # Password Confirmation Check
        if user['password'] != user['confirm_password']:
            flash(u"Passwords must match", "registration")
            is_valid = False

        return is_valid