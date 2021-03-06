from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
import re
from flask_app.models.pedal import Pedal
import pprint
import os
from decouple import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import mail


EMAIL_REGEX = re.compile((r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'))

db = 'dream_board_customs_2'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        if len(result) <1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) <1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_user(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        if len(results) >= 1:
            flash("Email already taken")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address")
            is_valid = False
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match!")
            is_valid = False
        return is_valid
