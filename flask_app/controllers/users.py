from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.question import Question
from flask_app.models.answer import Answer
import datetime

@app.route('/')
def index():
    if not 'id' in session:
        return render_template('index.html')
    elif session['id'] > 0:
        return redirect('/questions')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    if not User.check_login(request.form):
        return redirect('/')
    else:
        return redirect('/questions')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    else:
        data = {
            'username': request.form['username'],
            'email': request.form['email'],
            'password': request.form['password']
        }
        session['id'] = User.registration(data)
    return redirect('/questions')

@app.route('/questions')
def questions():
    if not 'id' in session:
        return redirect('/')
    elif session['id'] > 0:
        data = {
            'user': User.select(data={'id': session['id']}),
            'users': User.select(),
            'unanswered_questions': Question.unanswered_questions(),
            'answered_questions': Answer.answered_questions()
        }
        return render_template('questions.html', **data)

@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('/questions')
