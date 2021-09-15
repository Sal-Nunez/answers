from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
import re
from flask_bcrypt import Bcrypt
from flask_app.models import question
app = Flask(__name__)
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]\S*$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.questions = []
        
    @classmethod
    def select(cls, data=None):
        if data:
            query = "SELECT * FROM users left join questions on users.id = questions.user_id WHERE users.id = %(id)s"
            results = connectToMySQL('answers').query_db(query, data)
            user = cls(results[0])
            user.questions = []
            for question1 in results:
                if question1['question']:
                    data = {
                        'id': question1['questions.id'],
                        'question': question1['question'],
                        'description': question1['description'],
                        'created_at': question1['questions.created_at'],
                        'updated_at': question1['questions.updated_at'],
                        'user_id' : question1['user_id'],
                        'username': question1['username'],
                        'best_answer_id': question1['best_answer_id']
                    }
                    user.questions.append(question.Question(data))
                else:
                    break
            return user
        else:
            query = "SELECT * FROM users"
            results = connectToMySQL('answers').query_db(query)
            users = []
            for user in results:
                users.append(cls(user))
            return users
    @classmethod
    def check_login(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s"
        results = connectToMySQL('answers').query_db( query, data )
        user = cls(results[0])
        if user.email == data['email'] and bcrypt.check_password_hash(user.password, data['password']):
            print("TRUE")
            session['id'] = user.id
            return True
        else:
            print("FALSE")
            flash("Incorrect email/password try again", 'login')
            return False
    
    @classmethod
    def registration(cls, data):
        data['password'] = bcrypt.generate_password_hash(data['password'])
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s)"
        results = connectToMySQL('answers').query_db(query, data)
        if query:
            session['id'] = results
        return results


    @staticmethod #login validation
    def validate_login(data):
        is_valid = True
        query1 = "select * from users where users.email = %(email)s"
        if not connectToMySQL('answers').query_db(query1, data):
            flash("Email doesn't exist", 'login')
            is_valid = False
        if len(data['email']) < 7:
            flash('Email must be at least 7 characters', 'login')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email Address!", 'login')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', 'login')
            is_valid = False
        str1 = data['password']
        digits = 0
        uppers = 0
        for i in str1:
            if i.isdigit():
                digits += 1
            if i.isupper():
                uppers += 1
        if digits == 0:
            flash ('Password MUST contain at least one number!', 'login')
            is_valid = False
        if uppers == 0:
            flash ('Password MUST contain at least ONE capital letter!', 'login')
            is_valid = False
        return is_valid
    
    @staticmethod #registration validation
    def validate_register(data):
        is_valid = True
        if not data['password_confirmation'] == data['password']:
            flash('Passwords Do Not Match', 'registration')
            is_valid = False
        if len(data['email']) < 7:
            flash('Email must be at least 7 characters', 'registration')
            is_valid = False
        if not NAME_REGEX.match(data['username']):
            flash ("Username can only contain letters", 'registration')
        if len(data['username']) < 5:
            flash("Username MUST be at least 5 characters long", 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email Address!", 'registration')
            is_valid = False
        query1 = "select * from users where users.email = %(email)s"
        if connectToMySQL('answers').query_db(query1, data):
            flash("Email already exists, please Login, if you forgot your password TOUGH", 'registration')
            is_valid = False
        query2 = "select * from users where users.username = %(username)s"
        if connectToMySQL('answers').query_db(query2, data):
            flash("Username already exists, please Login, if you forgot your password TOUGH", 'registration')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', 'registration')
            is_valid = False
        str1 = data['password']
        digits = 0
        uppers = 0
        for i in str1:
            if i.isdigit():
                digits += 1
            if i.isupper():
                uppers += 1
        if digits == 0:
            flash ('Password MUST contain at least one number!', 'registration')
            is_valid = False
        if uppers == 0:
            flash ('Password MUST contain at least ONE capital letter!', 'registration')
            is_valid = False
        return is_valid