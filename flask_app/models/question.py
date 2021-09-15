from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash, session
import datetime
from flask_app.models import answer

class Question:
    def __init__(self, data):
        self.id = data['id']
        self.question = data['question']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.username = data['username']
        self.best_answer_id = data['best_answer_id']
        self.answers = []

    @classmethod
    def select(cls, data=None):
        if data:
            query = "SELECT *, COUNT(answers.id) as votes FROM questions left JOIN answers ON questions.id = answers.question_id left join users on users.id = questions.user_id left join users as users2 on users2.id = answers.user_id left join votes on answers.id = votes.answer_id WHERE questions.id = %(id)s"
            results = connectToMySQL('answers').query_db(query, data)
            question = cls(results[0])
            question.answers = []
            for answer1 in results:
                data = {
                    'id': answer1['answers.id'],
                    'answer': answer1['answer'],
                    'created_at': answer1['answers.created_at'],
                    'updated_at': answer1['answers.updated_at'],
                    'user_id': answer1['user_id'],
                    'question_id': answer1['question_id'],
                    'username': answer1['users2.username'],
                    'votes': answer1['votes']
                }
                question.answers.append(answer.Answer(data))
            
            return question
        else:
            query = "SELECT * FROM questions"
            results = connectToMySQL('answers').query_db(query)
            questions = []
            for question in results:
                questions.append(cls(question))
            return questions
    @classmethod
    def unanswered_questions(cls):
        query = "SELECT * FROM questions join users on questions.user_id = users.id left join answers on questions.id = answers.question_id group by questions.id"
        results = connectToMySQL('answers').query_db(query)
        if results:
            questions = []
            for question in results:
                if question['answer'] == None:
                    data = {
                        'id': question['id'],
                        'question': question['question'],
                        'description': question['description'],
                        'created_at': question['created_at'],
                        'updated_at': question['updated_at'],
                        'user_id': question['user_id'],
                        'username': question['username'],
                        'best_answer_id': question['best_answer_id'],
                    }
                    questions.append(cls(data))
            return questions
        else:
            return None
    @classmethod
    def new_question(cls, data):
        query = "INSERT INTO questions (question, description, user_id) VALUES (%(question)s, %(description)s, %(user_id)s)"
        return connectToMySQL('answers').query_db(query, data)

    @classmethod
    def edit_question(cls, data):
        query = "UPDATE questions SET question = %(question)s, description = %(description)s WHERE questions.id = %(id)s"
        return connectToMySQL('answers').query_db(query, data)

    @classmethod
    def delete(cls, data):
        print(data)
        query = "delete from questions where questions.id = %(id)s"
        return connectToMySQL('answers').query_db(query, data)
    
    @classmethod
    def best_answer(cls, data):
        query = "UPDATE questions set best_answer_id = %(answer_id)s where questions.id = %(question_id)s"
        return connectToMySQL('answers').query_db(query, data)